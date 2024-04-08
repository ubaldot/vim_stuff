vim9script
# Tell vim where is Python. OBS: this is independent of the plugins!
# You must check in the vim version what dll is required in the field -DDYNAMIC_PYTHON_DLL=\python310.dll\

setlocal foldmethod=indent


def Black(textwidth: number)
        var win_view = winsaveview()
        exe $":%!black - -q 2>{g:null_device} --line-length {textwidth}
                    \ --stdin-filename {shellescape(expand("%"))}"
        winrestview(win_view)
enddef

# Call black to format 120 line length
command! Black120 call Black(120)

# Manim stuff
command! -nargs=* -complete=customlist,ManimComplete Manim Manim(<f-args>)

def Manim(scene: string, quality = 'low_quality')
  if has("mac")
    exe "!osascript ~/QuickTimeClose.scpt"
  endif

  var flags = ""
  if quality ==# 'low_quality'
      flags = "-pql"
  elseif quality ==# 'high_quality'
      flags = "-pqh -c ~/Documents/YouTube/ControlTheoryInPractice/github_ctip/ctip_manim.cfg"
  elseif quality ==# 'transparent'
      flags = "-pqh -c ~/Documents/YouTube/ControlTheoryInPractice/github_ctip/ctip_manim.cfg --transparent"
  elseif quality ==# 'dry_run'
       flags = "--dry-run"
  endif

  &l:makeprg = $'manim {expand("%:t")} {scene} {flags} --fps 30 --disable_caching -v WARNING --save_sections'
  make
enddef


def ManimComplete(current_arg: string, command_line: string, cursor_position: number): list<string>
  # You call a command as :Foo arg1 arg2 and you want to select arg1 arg2 from
  # different lists. What we do is find the number of argument and then call
  # the appropriate function that returns the appropriate list.

  # This function is called when you hit tab.
  # We split the current command line in pieces separated by spaces, e.g. if
  # ':Foo ar' is called, then we have ['Foo', 'ar']. The string 'ar' may be
  # a leading argument of a command that user started to write, so even if the list has
  # length 2, then n shall be still 0 (we are editing the first argument)
  var parts = split(command_line[0 : cursor_position - 1], '\s\+')
  var arg_passed = empty(current_arg) ? 0 : 1
  # arg_number shall be the argument number that we want to edit, so we get
  # rid off everything before Foo and eventually of leading args
  var arg_number = len(parts) - index(parts, 'Manim') - arg_passed - 1

  var funcs = ['ManimSceneCompletion', 'ManimQualityCompletion']
  return call(funcs[arg_number], [current_arg])
enddef

def ManimSceneCompletion(arglead: string): list<string>
    var class_names = []
    var class_name = ""

    # Iterate through each line of the Python file
    for line in getline(1, line('$'))
        # Check if the line defines a class (a simple check for 'class <class_name>:')
        if line =~# '^\s*class\s\+\(\w\+\)'
            # Extract the class name and append it to the list
            # class_name = matchstr(line, '\s\+\(\w\+\)')
            # \zs start of the match, \ze end of the match
            class_name = matchstr(line, '^\s*class\s\+\zs\w\+\ze')
            add(class_names, class_name)
        endif
    endfor
    return class_names->filter($'v:val =~ "^{arglead}"')
enddef

def ManimQualityCompletion(arglead: string): list<string>
    var quality = ['low_quality', 'high_quality', 'dry_run', 'transparent']
    return quality->filter($'v:val =~ "^{arglead}"')
enddef

# Jump to next-prev section
nnoremap <buffer> <c-m> /\<self.next_section\><cr>
nnoremap <buffer> <c-n> ?\<self.next_section\><cr>
