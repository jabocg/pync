# PYNC - The Python File Sync

**NOTE:** This program is *very* early in its development lifetime. At this current point in time, it will copy files from 1 directory to another, assuming it matches this criterea:

- the destination file does not exist
- if it does exist, they are not the same AND the source file is newer

Planned Features:

- [ ] .pyncignore file
- [ ] "run and forget" style, automatically checking for modifications in the source directory
- [ ] arguments?
    --debug: provides aditional output, lines per file, ctime, etc
    --source: give source directory to create background process(look into)
    --dest: give dest directory to create background process(look into)
    --verbose -v: maybe more info about files, which ones check etc.
    --no-action -n: only list what WOULD happen, don't actually copy
- [ ] actual sync ability:
* define two directories in a file (.pynconf?) and sync them, keep them the same, auto detect modifications

