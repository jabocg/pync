# PYNC - The Python File Sync

**NOTE:** This program is *very* early in its development lifetime. At this 
current point in time, it will copy files from 1 directory to another, assuming
it matches this criterea:

- the destination file does not exist
- if it does exist, they are not the same AND the source file is newer

Planned Features:

- [ ] .pyncignore file
~~    * this mostly works, or so I thought, needs more work~~
    * implemented
- [ ] "run and forget" style, automatically checking for modifications in the
    source directory
- [x] arguments
    ~~
    * --debug: provides aditional output, lines per file, ctime, etc
        * might deprecate, just use verbose
            ~~
        * deprecated, using verbose
    * --source: give source directory to create background process(look into)
        * implemented
    * --dest: give dest directory to create background process(look into)
        * implemented
    * --verbose -v: maybe more info about files, which ones check etc.
        * implemented
    * --no-action -n: only list what WOULD happen, don't actually copy
        * implemented
            ~~
    * --ignore-file: specify the ignore file, without defaults to ~/.pyncignore
        * not focusing on for now, just use ~/.pyncignore
            ~~
        * deprecated, not needed
    * --quiet -q: opposite of verbose, don't output anything(except errors?)
        * implemented
- [ ] actual sync ability:
    * define two directories in a file (.pynconf?) and sync them, keep them 
        the same, auto detect modifications
- [ ] errors to output
- [ ] within the sync, detect DELETION of a file
- [ ] look into `rpyc` for a "daemon" like workings
    * allows the creation of background access
    * probable have it so where if a bgprc does not exist, create it

**Self Note:** using `if` and `if not` are 'shallow' copies. Use `==` and `!=` 
instead.
