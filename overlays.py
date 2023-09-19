import manim as mn  # type:ignore
import numpy as np  # type:ignore
from scipy.io import wavfile
import sys


sys.path.append("/users/ubaldot/.manim")
import myconfig as mycfg  # type:ignore


class Temperature(mn.Scene):
    def setup(self):
        pass
        # self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        MAKE_SMOOTH = True

        self.next_section("Scroll signal", skip_animations=False)

        # Generic signal
        N = 288
        signal = np.random.default_rng().uniform(10, 28, N)
        Ts = 0.1

        # Low pass filter data
        Tc = 1.8  # Tc = 1/Fc, OBS! Tc>Ts
        signal_filt = np.zeros(len(signal))
        signal_filt[0] = signal[0]
        for ii, s in enumerate(signal[1:]):
            signal_filt[ii + 1] = (1 - Ts / Tc) * signal_filt[ii] + Ts / Tc * s

        axis_config_others = {
            "y_range": [0, 32, 32 / 10],
            "x_length": 11.0,
            "y_length": 6.0,
        }
        x_span = 5
        x_range = [0.0, x_span, 1]
        ax = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others)
        # x_label = ax.get_x_axis_label(mn.MathTex(r"\textrm{time [s]}", font_size=28), edge=mn.DR)
        # y_label = ax.get_y_axis_label(mn.MathTex("^\circ C").scale(0.45), edge=mn.UL)
        x_label = mn.MathTex(r"\textrm{time [h]}", font_size=28).next_to(ax, mn.DOWN, buff=0.2)
        y_label = (
            mn.MathTex(r"\textrm{Temperature [}^\circ \textrm{C}]}", font_size=28)
            .rotate(90 * mn.DEGREES)
            .next_to(ax, mn.LEFT, buff=0.2)
        )

        # Convert the direction [Ts,0,0] to POINTS
        STEP_DIR = ax.c2p(Ts, 0) - ax.c2p(0, 0)
        self.add(mn.VGroup(ax, x_label, y_label))

        # INIT
        current_time = 0
        P0 = ax.c2p(current_time, signal_filt[0])
        current_time += Ts
        P1 = ax.c2p(current_time, signal_filt[1])
        signal_displayed = mn.Line(P0, P1)
        value_tex = mn.MathTex(f"{np.round_(signal_filt[1],1)}^\circ C", font_size=28).move_to(
            signal_displayed.get_end(), mn.RIGHT
        )
        self.add(signal_displayed, value_tex)
        self.add(signal_displayed)
        self.wait(Ts)

        # ITERATIONS
        for ii, _ in enumerate(signal_filt[1:]):
            # for ii in range(0):
            # Scroll once the plot reaches the displayed max x.
            if current_time + Ts > x_range[1]:
                x_range[0] += Ts
                x_range[1] += Ts

            ax_new = mn.Axes(
                axis_config=mycfg.axis_config,
                **axis_config_others,
                x_range=x_range,
            )

            # Update Axes
            self.remove(ax)
            self.add(ax_new)
            ax = ax_new

            # Display signal_filt
            if current_time + Ts < x_span or np.isclose(current_time + Ts, x_span):
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))
            else:
                signal_displayed.shift(-STEP_DIR)
                signal_displayed.points = signal_displayed.points[4:]
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))

            if MAKE_SMOOTH:
                signal_displayed.make_smooth()

            # Update number
            value_tex_new = mn.MathTex(f"{np.round_(signal_filt[ii],1)}^\circ C", font_size=28).next_to(
                signal_displayed.get_end(), mn.RIGHT
            )
            value_tex.become(value_tex_new)

            current_time += Ts
            self.wait(Ts)
        self.wait(Ts)


class BirdChirp(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        MAKE_SMOOTH = True

        self.next_section("Scroll signal", skip_animations=False)

        # Bird chirp
        wav_fname = "/users/ubaldot/Downloads/BirdAudio.wav"
        fs, data = wavfile.read(wav_fname)
        # Pick one sample every 4800 and normalize
        step = int(2400 * 2)  # OBS This depends on the FPS! Ts cannot be too small!
        Ts = step / fs  # Ts > 2/fps
        print(Ts)
        signal_filt = data[1::step, 0] / max(data[1::step, 0])
        print(len(signal_filt))

        axis_config_others = {
            "y_range": [-1, 1, 1 / 10],
            "x_length": 11.0,
            "y_length": 6.0,
        }
        x_span = 5
        x_range = [0.0, x_span, x_span / 10]
        ax = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others)
        # x_label = ax.get_x_axis_label(mn.MathTex(r"\textrm{time [s]}", font_size=28), edge=mn.DR)
        # y_label = ax.get_y_axis_label(mn.MathTex("^\circ C").scale(0.45), edge=mn.UL)
        x_label = mn.MathTex(r"\textrm{time [s]}", font_size=28).next_to(ax, mn.DOWN, buff=0.2)
        y_label = mn.MathTex(r"\textrm{Amplitude}", font_size=28).rotate(90 * mn.DEGREES).next_to(ax, mn.LEFT, buff=0.2)

        # Convert the direction [Ts,0,0] to POINTS
        STEP_DIR = ax.c2p(Ts, 0) - ax.c2p(0, 0)
        self.add(mn.VGroup(ax, x_label, y_label))

        # INIT
        current_time = 0.0
        P0 = ax.c2p(current_time, signal_filt[0])
        current_time += Ts
        P1 = ax.c2p(current_time, signal_filt[1])
        signal_displayed = mn.Line(P0, P1)
        self.add(signal_displayed)
        self.wait(Ts)

        # ITERATIONS
        for ii, _ in enumerate(signal_filt[1:]):
            # for ii in range(0):
            # Scroll once the plot reaches the displayed max x.
            if current_time + Ts > x_range[1]:
                x_range[0] += Ts
                x_range[1] += Ts

            ax_new = mn.Axes(
                axis_config=mycfg.axis_config,
                **axis_config_others,
                x_range=x_range,
            )

            # Update Axes
            self.remove(ax)
            self.add(ax_new)
            ax = ax_new

            # Display signal_filt
            if current_time + Ts < x_span or np.isclose(current_time + Ts, x_span):
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))
            else:
                signal_displayed.shift(-STEP_DIR)
                signal_displayed.points = signal_displayed.points[4:]
                signal_displayed.add_line_to(ax.c2p(current_time + Ts, signal_filt[ii]))

            if MAKE_SMOOTH:
                signal_displayed.make_smooth()

            current_time += Ts
            self.wait(Ts)
        self.wait(Ts)


class ScrollSignalWithUpdater(mn.Scene):
    def construct(self):
        Ts = 0.1
        N = 200
        times = [t for t in np.linspace(0, N * Ts, N)]
        signal = np.random.default_rng().uniform(20, 28, N)
        Ts = 0.2
        Tc = 1.8  # Tc = 1/Fc, OBS! Tc>Ts

        # Low pass filter data
        data = np.zeros(len(signal))
        data[0] = signal[0]
        for ii, s in enumerate(signal[1:]):
            data[ii + 1] = (1 - Ts / Tc) * data[ii] + Ts / Tc * s

        # Bird chirp
        wav_fname = "/users/ubaldot/Downloads/BirdAudio.wav"
        fs, data = wavfile.read(wav_fname)
        # Pick one sample every 4800 and normalize
        step = 2400  # OBS This depends on the FPS! Ts cannot be too small!
        Ts = step / fs
        print(Ts)
        data = data[1::step, 0] / max(data[1::step, 0])
        N = len(data)
        times = [t for t in np.linspace(0, N * Ts, N)]

        time = mn.ValueTracker(0)
        trange = 5.05  # OBS! trange/Ts shall not be an integer!

        plot = mn.VMobject()
        ax = mn.VMobject()
        value = mn.VMobject()
        graph = mn.VGroup(ax, plot, value)

        def graph_updater(vgrp):
            startt = max(time.get_value() - trange, 0)
            ax, plot, value = vgrp

            # Moving window of size trange. The window move with the ValueTracker. OBS! trange/Ts shall not be an integer!
            tempts = [t for t in times if startt <= t <= time.get_value()]
            tempds = [d for i, d in enumerate(data) if startt <= times[i] <= time.get_value()]

            # New axis
            if time.get_value() > trange:
                tmin = tempts[0]
                tmax = tmin + trange
            else:
                tmin = 0.0
                tmax = trange

            ax_new = mn.Axes(
                x_range=[tmin, tmax, trange / 10],
                y_range=[-1, 1, 0.2],
                x_length=10,
                y_length=5,
                axis_config=mycfg.axis_config,
            ).add_coordinates()

            # New plot
            plot_new = ax_new.plot_line_graph(tempts, tempds, add_vertex_dots=False)

            # New value
            # value_new = mn.MathTex(f"{np.round_(tempds[-1],1)}^\circ C", font_size=28)

            ax.become(ax_new)
            plot.become(plot_new)
            # value.become(value_new)

        graph.add_updater(graph_updater, call_updater=True)

        x_label = mn.MathTex(r"\mathrm{time [s]}", font_size=28).next_to(graph[0], mn.DOWN, buff=0.2)
        y_label = (
            mn.MathTex(r"\mathrm{Volume}", font_size=28).rotate(90 * mn.DEGREES).next_to(graph[0], mn.LEFT, buff=0.2)
        )
        self.add(graph, x_label, y_label)
        self.play(time.animate.set_value(times[-1]), rate_func=mn.rate_functions.linear, run_time=times[-1])


class QuarterlyRevenue(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        mycfg.axis_config["font_size"] = 28
        y_range = [0, 100, 10]
        x_range = [0, 5, 1]
        ax = mn.Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=10,
            y_length=5,
            axis_config=mycfg.axis_config,
        ).add_coordinates()

        x_label = mn.MathTex(r"\textrm{Quarters}", font_size=36).next_to(ax, mn.DOWN, buff=0.2)
        y_label = (
            mn.MathTex(r"\textrm{Renevue [M€]}", font_size=36).rotate(90 * mn.DEGREES).next_to(ax, mn.LEFT, buff=0.3)
        )

        lines = mn.VGroup()
        for ii in range(*y_range):
            point = ax.c2p(x_range[1], ii)
            line = ax.get_horizontal_line(
                point, line_func=mn.DashedLine, line_config={"stroke_opacity": 0.4, "dash_length": 0.1}
            )
            lines.add(line)

        Q1 = mn.Rectangle(height=0.01, width=1.2, fill_opacity=1.0).move_to(ax.c2p(1, 0), aligned_edge=mn.DOWN)
        Q2 = Q1.copy().move_to(ax.c2p(2, 0), aligned_edge=mn.DOWN)
        Q3 = Q1.copy().move_to(ax.c2p(3, 0), aligned_edge=mn.DOWN)
        Q4 = Q1.copy().move_to(ax.c2p(4, 0), aligned_edge=mn.DOWN)

        self.add(ax, x_label, y_label, Q1, Q2, Q3, Q4, lines)

        Q1.generate_target()
        Q1.target.stretch_to_fit_height(3, about_edge=mn.DOWN)

        Q2.generate_target()
        Q2.target.stretch_to_fit_height(2.1, about_edge=mn.DOWN)

        Q3.generate_target()
        Q3.target.stretch_to_fit_height(4.2, about_edge=mn.DOWN)

        Q4.generate_target()
        Q4.target.stretch_to_fit_height(2.6, about_edge=mn.DOWN)
        self.play(mn.MoveToTarget(Q1), mn.MoveToTarget(Q2), mn.MoveToTarget(Q3), mn.MoveToTarget(Q4), run_time=3)
        self.wait()


class Discretization_Quantization(mn.Scene):
    def setup(self):
        self.add(mycfg.imageBG)
        # plane = mn.NumberPlane()
        # self.add(plane)

    def construct(self):
        # Generic signal
        N = 50
        signal = np.random.default_rng().uniform(-2, 2, N)
        Ts = 0.1
        times = np.linspace(0.0, N * Ts, N)

        # Low pass filter data
        Tc = 0.2  # Tc = 1/Fc, OBS! Tc>Ts
        signal_filt = np.zeros(len(signal))
        signal_filt[0] = signal[0]
        for ii, s in enumerate(signal[1:]):
            signal_filt[ii + 1] = (1 - Ts / Tc) * signal_filt[ii] + Ts / Tc * s

        mycfg.axis_config["font_size"] = 32
        y_range = [-1.9, 2, 1]
        axis_config_others = {
            "y_range": y_range,
            "x_length": 12.0,
            "y_length": 5.5,
        }
        x_span = N * Ts
        x_range = [0.0, x_span, 0.5]
        ax = mn.Axes(axis_config=mycfg.axis_config, x_range=x_range, **axis_config_others)
        x_label = ax.get_x_axis_label(mn.Text("time", font_size=28), edge=mn.DR)
        continuous_points = [ax.c2p(_x, _y) for _x, _y in zip(times, signal_filt)]
        continuous_signal = mn.VMobject().set_points_smoothly(continuous_points)

        self.next_section("Discretization", skip_animations=False)
        # Sampling perios
        Tss = 0.5
        sampling_times = times[0 :: int(Tss / Ts)]
        samples = signal_filt[0 :: int(Tss / Ts)]
        discrete_points = [ax.c2p(_x, _y, 0) for _x, _y in zip(sampling_times, samples)]
        Dots = mn.VGroup()
        for p in discrete_points:
            Dots.add(mn.VGroup(ax.get_vertical_line(p), mn.Dot(p, color=mn.TEAL)))

        label0 = mn.MathTex(rf"Sampling\quad(T_s = {Tss})").to_edge(mn.DOWN)
        self.play(mn.Write(mn.VGroup(ax, x_label)))
        self.wait()
        self.play(mn.Write(continuous_signal))
        self.wait()
        self.play(mn.Write(label0))
        self.wait()
        self.play(mn.Write(Dots))
        self.wait()
        self.play(mn.FadeOut(continuous_signal))
        self.wait()
        self.play(mn.FadeOut(label0, Dots))
        self.wait()
        self.play(mn.FadeIn(continuous_signal))
        self.wait(1)

        Delta = 0.2
        label1 = mn.MathTex(rf"Quantization\quad(\Delta = {Delta})").to_edge(mn.DOWN)

        quantization_lines = mn.VGroup()
        q_bins = np.arange(y_range[0], y_range[1], Delta)
        for y in q_bins:
            quantization_lines.add(ax.get_horizontal_line(ax.c2p(x_span, y)))

        brace = mn.BraceBetweenPoints(
            quantization_lines[16].get_end(), quantization_lines[17].get_end(), buff=0
        ).stretch_to_fit_width(0.1)
        delta_tex = mn.MathTex(r"\Delta", font_size=32).next_to(brace, mn.RIGHT, buff=0.05)

        self.play(mn.ReplacementTransform(label0, label1))
        self.play(mn.FadeIn(quantization_lines, brace, delta_tex))
        self.wait()

        self.next_section("Quantization", skip_animations=False)

        # Quantize values
        q_signal = np.empty_like(signal_filt)
        for ii, val in enumerate(signal_filt):
            closest_value = min(q_bins, key=lambda x: np.abs(x - val))
            q_signal[ii] = closest_value
        quantized_points = [ax.c2p(_x, _y) for _x, _y in zip(times, q_signal)]

        quantized_curve = mn.VMobject(color=mn.YELLOW)
        t_step = quantized_points[1][0] - quantized_points[0][0]
        for ii in range(len(quantized_points) - 1):
            x0, y0, _ = quantized_points[ii]
            x1, y1, _ = quantized_points[ii + 1]
            l0 = mn.Line((x0, y0, 0), (x0 + t_step / 2, y0, 0))
            l1 = mn.Line((x0 + t_step / 2, y0, 0), (x0 + t_step / 2, y1, 0))
            l2 = mn.Line((x0 + t_step / 2, y1, 0), (x0 + t_step, y1, 0))
            quantized_curve.append_vectorized_mobject(l0)
            quantized_curve.append_vectorized_mobject(l1)
            quantized_curve.append_vectorized_mobject(l2)

        self.add(quantized_curve)
        self.play(mn.FadeIn(quantized_curve))
        self.play(mn.FadeOut(continuous_signal, brace, delta_tex))
        self.wait()

        self.next_section("Sampling and quantization", skip_animations=False)

        q_Dots = mn.VGroup()
        quantized_samples = q_signal[0 :: int(Tss / Ts)]
        quantized_sampled_points = [ax.c2p(_x, _y, 0) for _x, _y in zip(sampling_times, quantized_samples)]
        for p in quantized_sampled_points:
            x0 = p[0]
            y0 = ax.c2p(0, y_range[0], 0)[1] - 0.1
            y1 = ax.c2p(0, y_range[1], 0)[1] + 0.1
            q_Dots.add(mn.VGroup(mn.DashedLine((x0, y0, 0), (x0, y1, 0), stroke_opacity=0.4), mn.Dot(p, color=mn.RED)))

        label2 = mn.MathTex(
            rf"Quantization\,(\Delta = {Delta})\quad and \quad Sampling\,(T_s = 0.5)", font_size=36
        ).to_edge(mn.DOWN)

        self.play(mn.ReplacementTransform(label1, label2))
        self.play(mn.FadeIn(q_Dots))
        self.wait()
        self.play(mn.FadeOut(quantized_curve))
        self.wait()


class Quantization(mn.Scene):
    def construct(self):
        N = 10
        Ts = 0.5
        y_values = np.random.default_rng().uniform(-2, 2, N)
        x_values = np.linspace(np.ceil(-N * Ts), np.floor(N * Ts), N)
        points = [(x, y, 0) for x, y in zip(x_values, y_values)]

        zoh_curve = mn.VMobject(color=mn.TEAL)
        t_step = x_values[1] - x_values[0]
        for ii in range(len(points) - 1):
            x0, y0, z0 = points[ii]
            x1, y1, z0 = points[ii + 1]
            l0 = mn.Line((x0, y0, z0), (x0 + t_step / 2, y0, z0))
            l1 = mn.Line((x0 + t_step / 2, y0, z0), (x0 + t_step / 2, y1, z0))
            l2 = mn.Line((x0 + t_step / 2, y1, z0), (x0 + t_step, y1, z0))
            zoh_curve.append_vectorized_mobject(l0)
            zoh_curve.append_vectorized_mobject(l1)
            zoh_curve.append_vectorized_mobject(l2)

        self.add(zoh_curve)

        # Alternative
        steps = []
        for x, x_next, y in zip(x_values, x_values[1:], y_values):
            steps.append([x, y, 0])
            steps.append([x_next, y, 0])
        steps.append([x_values[-1], y_values[-1], 0])

        curve = mn.VMobject().set_points_as_corners(steps)
        curve2 = mn.VMobject().set_points_as_corners(points).set_color(mn.RED)
        self.add(curve, curve2, zoh_curve)


class StreamLine(mn.Scene):
    def setup(self):
        img = (
            mn.ImageMobject("Pianta")
            .stretch_to_fit_width(mn.config.frame_width)
            .stretch_to_fit_height(mn.config.frame_height)
        )
        self.add(img)
        # self.add(mycfg.imageBG)
        plane = mn.NumberPlane()
        self.add(plane)

    def construct(self):
        def func(x):
            x_eq = np.array((2, 2))
            xdot = np.array([[1, 2], [-2, 1]]) @ (x[0:2] - x_eq)
            return np.array((xdot[0], xdot[1], 0))

        stream_lines = mn.StreamLines(
            func,
            max_anchors_per_line=20,
            opacity=0.8,
            stroke_width=2,
            max_color_scheme_value=2,
            colors=["#FFFFFF", "#FFFFFF"],
            virtual_time=5,
        )
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=0.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)


# vim: set textwidth=120:
