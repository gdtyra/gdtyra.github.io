# Unix Commands

This is a collection of notes relating to commands that are available in Linux and most Unix-like environments. In many cases only useful examples of a command are listed without a proper explanation of the command in general.

## `tar` - manipulate tar files
- `tar -czf <archive> <directory>` - create a gzip-compressed archive containing the given directory
- `tar -chzf <archive> <directory>` - same as above, but dereference any symbolic links and archive the target file
- `tar -cf <archive> -C <directory> <file1> <file2>` - create an uncompressed archive containing two files relative to the given directory
- `tar -xf <archive> -C <directory> <file1> <file2>` - extract 2 files from the archive into the given directory
- `tar -taf <archive>` - list files in the archive and automatically determine the compression scheme

## `find` - find files and directories matching criteria
* `-L` follow symlinks
- `-type <f,d,l>` - include only files, directories, or links respectively
* `-name <glob>` - filter file name by glob pattern
* `-path <glob>` - filter by glob pattern against entire path
* `-print` - print matching file paths
* `-depth` - process directory contents before directory itself
* `-maxdepth <n>` - limit depth of search
* `-mindepth <n>` - ignore shallow files
* `-exec <command> \;` - run a command for each result where `\;` marks the end of the command and `{}` optionally specifies where arguments are placed
* `-print0` - output null-terminated paths for use with `xargs`
- `find . -type f -exec grep "pattern" {} \;` - find files that match pattern
- `find <file1> -newer <file2> -print` - print the newer of two files
- `find tmp -maxdepth 1 -name *.mp3 -print0 | xargs -0 rm` - delete MP3 files that are 1 level deep within `tmp`

## `xargs` - treat input as arguments to a command
- `-n <n>` - limit args per instance of command. Often `-n 1` is needed when a command accepts only one file
- `-L <n>` - limit lines of input per command. Often `-L 1` when each line of input corresponds to an instance of the command
- `-P <n>` - limit number of parallel commands, or `0` for unlimited
- `-I<symbol>` - symbol to replace with argument values in command, usually `{}`. Otherwise, they are placed at the end of the command
- `-0` - read input as null-terminated strings. Mainly used along with `find -print0`
- `xargs -n 1 -P 1 -I{} ssh -tt {} 'top -n 1 -b | grep "Cpu(s)"'` - `ssh` to hosts one at a time and run `top` on them
- `find . -name '*.wav' -print0 | xargs -0 md5sum` - find all WAV files and print their MD5 sums
- `cat old-archive-ids | xargs -L1 -I{} ./delete.sh {}` - run a script once for each line in a file 

## `basename` and `dirname` - remove prefix and suffix from file paths
- `basename path/to/file.txt` - yields `file.txt`
- `basename path/to/file.txt .txt` - yields `file`
- `basename -a -s .txt file1.txt file2.txt` - yields `file1\nfile2`
- `dirname path/to/file.txt` - yields `path/to`
- `dirname path/to/` - yields `path`
- `dirname path/to` - yields `path`

## `sed` - manipulate text line-wise
- `sed -n <n>p` - print only line `n` of the input
- `sed -e '2,$d'` - delete all but first line of input
- `sed -e "/^FirstKeyword\$/,/^SecondKeyword\$/d"` - delete lines once `FirstKeyword` is seen until after `SecondKeyword` is seen
- `sed -e "/^FirstKeyword\$/,/^SecondKeyword\$/!d"` - the opposite of the above; keep only lines between and including the two keywords
- `sed 's/Counters=\(.*\)$/\1/'` - keep only the value of `Counters`
- `sed 's/,/\n/g'` - replace all commas with newlines
- `sed -r 's/(^|_)([a-z])/\U\2/g'` - UpperCamelCase a string
- `sed 's/^.*customerId.{"s":"\([A-Z0-9]*\)"}.*$/\1 &/g'` - capture ID value and copy it to the front of the line
* `find src -name '*.c' -exec sed -i 's/= OLD_MACRO(\(\w*\))\[\(.*\)\]/= NEW_MACRO(\1, \2)/' {} \;` - in each C file, replace a particular macro usage of the form `OLD_MACRO(foo)[bar]` with `NEW_MACRO(foo, bar)`

## `tr` - delete or replace characters
- `tr '[A-Z]' '[a-z]'` - replace all upper case letters with lower case
- `tr -d '"'` - remove all double-quotes
- `tr -s '\t' ','` - replace tabs with commas

## `cmp` - compare files byte-wise
- `cmp -s <file1> <file2>` - exits non-zero if files are not the same

## `pr` and `paste` - join files column-wise
- `pr -m -t <file1> <file2>` - prints files side-by-side
- `paste <file1> <file2>` - prints files side-by-side

## `comm` - some set operations on sorted files
- `comm -12 <sorted_file_1> <sorted_file_2>` - outputs lines common to both files
- `comm -23 <sorted_file_1> <sorted_file_2>` - outputs lines unique to the first file
- `comm -3 <sorted_file_1> <sorted_file_2>` - outputs lines that are unique to either file

## `dd` - read and write files or devices byte-wise
- `dd if=<file> ibs=1 skip=200 count=100` - read 100 bytes starting at the 200th byte
- `dd if=/dev/sdf of=image.bin bs=8M` - write the entire device `/dev/sdf` to a file with a block size of 8M

## `sudo` - execute commands as a different user
- The `-E` flag will preserve your current environment when running the command
- Using `--preserve-env=<list>` will preserve only the listed environment variables

## `kill` and `pkill` - terminate processes or send signals
- `kill <pid>`, `kill -15 <pid>`, or `kill -TERM <pid>` - ask a process to stop gracefully
- `kill -9 <pid>` or `kill -KILL <pid>` - force-kill a process by PID
- `pkill -KILL -f <part_of_process_name>` - force-kill processes with a name that includes the given string

### Other signals

`kill` is most commonly used with the `TERM` and `KILL` signals, but there are others that a given process may or may not respond to:

- `HUP` - sometimes causes a daemon or service to reload its configuration files
- `INT` - equivalent to pressing `Ctrl+C` in a terminal
- `ALRM` - represents a timed event
- `QUIT` and `ABRT` - similar to `INT` but often used to generate a core dump
- `STOP` and `CONT` - used to pause and resume a process respectively

## `stat` and `readlink` - print file information

The `stat` command is not compatible between Linux and BSD / macOS, unfortunately, so `readlink` may be a better option for the specific use case of resolving a link to its target.

- `stat -f '%Y' <symbolic_link>` (BSD) or `readlink <symbolic_link>` (Both) - print target of a symbolic link
- `stat -f '%Lp' <file>` (BSD) or `stat -c '%a' <file>` (Linux) - print permission mask in octal form

## `tcpdump` - capture network traffic
- `tcpdump -A -vvv <some.endpoint.host>` - print TCP packets to and from the given host as ASCII with maximum verbosity

## `dig` - DNS lookup
- `dig <some.endpoint.host>` - view DNS resolution for the given host
- `dig -x <IP address>` - reverse DNS lookup to determine hostname for a given IP address

## `nc` - read and write TCP/UDP connections
- `nc <some.host.name> <port>` - open TCP connection
- `nc -u <some.host.name> <port>` - open UDP connection
- `nc -l <port>` - listen on a given port
- `nc -z <some.host.name> <port_range_start>-<port_range_end>` - attempt to connect on a range of ports and report which were open

## `tail` - print and follow ends of files
- `tail -f <file>` - print last lines of a file and print new lines as they are appended
- `tail -F <file>` - same as `-f` but deals with the named file being renamed or replaced by a new file

## `mount` - manage mounted filesystems
- `mount` - view currently mounted paths and filesystem types

## `watch` - run a command repeatedly to observe changes
- `watch -t <command>` - run command repeatedly with the default 2 second interval and hide the header
- `watch -n 60 <command>` - run command repeatedly every minute
- `watch -d <command>` - run command repeatedly and highlight differences between consecutive runs
- `watch --differences=permanent <command>` - run command repeatedly and highlight differences from initial run

## `rsync` - copy and mirror directory structures
- `-delete` - delete files that don't exist on sender (system)
- `-v` - verbose (`-vv` will provide more detailed information)
- `-e ssh <options>` - specify ssh with options for remote targets
- `-a` - archive mode which preserves permissions (owners, groups), times, symbolic links, and devices
- `-r` - recurse into directories
- `-z` - compress file data during transfer
- `--exclude <directory>` – excludes the given directory
- `-P` – show progress during the transfer
- `-n` - perform a dry-run without actually writing anything
- `-i` - show changes
- `-W` - transfer whole files; do not attempt a delta sync

If `/` is placed at the end of the source folder, `rsync` will copy only the content of the folder. Otherwise, it will copy the folder itself.  Similarly, if `/` is placed at the end of the destination folder, `rsync` will paste the data directly inside the folder. Otherwise, it will create a folder with that name and copy into it.

- `rsync -v -e ssh /home/localuser/testfile.txt remoteuser@X.X.X.X:/home/remoteuser/transfer` - copy a file from local to remote
- `rsync -r -a -v -e ssh --delete /home/localuser/testfolder remoteuser@X.X.X.X:/home/remoteuser/testfolder` - sync a local folder to remote with archival flags set and deleting files that don't exist locally

## `git` - *the* source control
- `git init` - initialize the current directory as a git repository
- `git add origin <uri>` - add an upstream remote repository
- `git fetch` - update information from the origin
- `git checkout -t origin/<branch>` - checkout a local copy of an upstream branch
- `git push origin :<branch>` - delete a remote branch
- `git checkout -b <local_name> --track origin/<branch_name>` - create a local branch tracking a remote one with a different name
- `git checkout -b <local_name>` - create a new local copy of the current branch
- `git push origin <change_id>:<branch>` - push local changes only up to a particular commit
- `git push -u origin <branch>` - regular push of local changes to remote branch
- `git clean -f -d` - remove local untracked files and directories
- `git reset --merge` - abort a merge that isn't going well
- `git reset --hard origin/<branch>` - discard committed changes that haven't yet been pushed
- `git branch -d <branch>` - delete a local branch
- `git diff HEAD~2 HEAD -- <paths...>` - compare paths between current and 2 revisions prior

## `ruby` - using Ruby for one-liners

Ruby has command-line options that make it useful for writing inline scripts as an alternative to `sed` or `awk`.

- `-F <pattern>` - specifies the input field separator (`$;`)
- `-n` - causes Ruby to add `while gets` around your script which makes it iterate over file name arguments somewhat like `sed -n` or `awk`
- `-p` - mostly the same as `-n`, but prints the value of `$_` at the each end of each loop
- `-a` - turns on auto-split mode when used with `-n` or `-p`. In auto-split mode, Ruby executes `$F = $_.split` at the beginning of each loop
- `-d` or `--debug` - turns on debug mode; `$DEBUG` will be set to true
- `-i <extension>` - specifies in-place-edit mode with an optional extension to be used for a backup copy
- `-l`- enables automatic line-ending processing, which sets `$\` to the value of `$/` and chops every line read using `chop!`
- `-e <ruby_statements>` - specifies script from command-line and causes Ruby not to search the rest of arguments for a script file name
- `-r <library>` - load the specified library using require.  It is useful when using `-n` or `-p`
- `ruby -p -e ’$_.tr! "a-z", "A-Z"’` - equivalent to `tr '[a-z]' '[A-Z]'`

### `ffmpeg` - media encoding
- `ffmpeg -framerate 30 -i "%d.bmp" -r 30 -pix_fmt yuv420p video.mp4` - create a video from a sequence of image files
- `ffmpeg -i original.jpg -qmin 1 -q:v 1 -vf "scale=iw/2:ih/2" reduced.jpg` - re-encode an image at half the resolution
- `ffmpeg -i video.mp4 -c:v null -c:a copy audio.m4a` - extract only the audio from an MP4 video
- `ffmpeg -i input.avi -vf 'yadif=1:1,drawbox=y=ih-h:w=0:h=11:t=max,hqdn3d=6' -acodec aac -vcodec libx264 -pix_fmt yuv420p -preset veryslow -crf 20 -aspect 4:3 output.mp4` - re-encode an interlaced, 4:3 AVI as an MP4 after masking overscan noise and denoising the image
- `ffmpeg -i input.avi -acodec copy -vcodec ffv1 -coder 1 -g 1 -context 1 -pix_fmt yuv410p output.avi` - re-encode as lossless FFV1
- `for f in **/*.wav; ./ffmpeg.exe -i "$f" flac/"$(basename $f .wav)".flac` - encode all WAV files in under the current path as FLAC and put the files under a "flac" directory

## Miscellaneous
- `cal` - display calendars
- `at` - schedule a task at a given time
- `fortune` - print random messages from a collection
- `diff` - compare files or directory structures
- `patch` - apply changes specified by a diff
- `tsort` - topologically sort a graph
- `od` - display files in hexadecimal or other forms
- `nohup` - prevent a program from stopping after logout
- `nl` - add line numbers to output
- `join` - join lines in files by shared field values 
- `bc` - do calculations
- `file` - heuristically determine file content type
- `fc` - deal with command history
- `csplit` - split a file into multiple based on context lines
- `split` - split a file into multiple files of a fixed size
- `fmt`, `fold` - apply word wrapping to text
- `banner`, `figlet`, and `cowsay` - print fancy text
- `pexec` and `parallel` - run commands concurrently
- `javap -classpath some_jar.jar some.package.SomeClass` - list method signatures of a class within a JAR file
- `tree <file>` - write input to both standard output and the given file
- `wget -O <output_path> <some.resource/address>` - download a given resource to a given path
- `chsh -s <shell_path> <user>` - change a user's login shell