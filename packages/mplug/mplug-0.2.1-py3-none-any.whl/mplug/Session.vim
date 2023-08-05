let SessionLoad = 1
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/Code/mplug
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +0 src/mplug/mplug.py
badd +0 src/mplug/util.py
badd +0 test/test_mplug.py
argglobal
%argdel
set stal=2
edit src/mplug/mplug.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 30 + 29) / 58)
exe 'vert 1resize ' . ((&columns * 114 + 77) / 155)
exe '2resize ' . ((&lines * 30 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 40 + 77) / 155)
argglobal
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=10
setlocal fml=1
setlocal fdn=10
setlocal fen
let s:l = 409 - ((22 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
409
normal! 015|
lcd ~/Code/mplug/src/mplug
wincmd w
argglobal
enew
file ~/Code/mplug/src/mplug/__Tagbar__.1
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=10
setlocal fml=1
setlocal fdn=10
setlocal nofen
lcd ~/Code/mplug/src/mplug
wincmd w
exe '1resize ' . ((&lines * 30 + 29) / 58)
exe 'vert 1resize ' . ((&columns * 114 + 77) / 155)
exe '2resize ' . ((&lines * 30 + 29) / 58)
exe 'vert 2resize ' . ((&columns * 40 + 77) / 155)
tabedit ~/Code/mplug/test/test_mplug.py
set splitbelow splitright
wincmd _ | wincmd |
split
1wincmd k
wincmd w
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
exe '1resize ' . ((&lines * 10 + 29) / 58)
exe '2resize ' . ((&lines * 44 + 29) / 58)
argglobal
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=10
setlocal fml=1
setlocal fdn=10
setlocal fen
let s:l = 63 - ((4 * winheight(0) + 5) / 10)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
63
normal! 036|
lcd ~/Code/mplug/src/mplug
wincmd w
argglobal
if bufexists("~/Code/mplug/test/test_mplug.py") | buffer ~/Code/mplug/test/test_mplug.py | else | edit ~/Code/mplug/test/test_mplug.py | endif
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=10
setlocal fml=1
setlocal fdn=10
setlocal fen
let s:l = 480 - ((22 * winheight(0) + 22) / 44)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
480
normal! 034|
lcd ~/Code/mplug/src/mplug
wincmd w
2wincmd w
exe '1resize ' . ((&lines * 10 + 29) / 58)
exe '2resize ' . ((&lines * 44 + 29) / 58)
tabedit ~/Code/mplug/src/mplug/util.py
set splitbelow splitright
wincmd t
set winminheight=0
set winheight=1
set winminwidth=0
set winwidth=1
argglobal
setlocal fdm=syntax
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=10
setlocal fml=1
setlocal fdn=10
setlocal fen
let s:l = 17 - ((8 * winheight(0) + 15) / 30)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17
normal! 031|
lcd ~/Code/mplug/src/mplug
tabnext 2
set stal=1
if exists('s:wipebuf') && getbufvar(s:wipebuf, '&buftype') isnot# 'terminal'
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=20 winminheight=1 winminwidth=1 shortmess=filnxtToOFI
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
