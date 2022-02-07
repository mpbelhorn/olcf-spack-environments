--Default modules to load upon
--  module refresh
--  module restore
--
-- should only load modules
-- should not include other commands that set/alter variables, path, ...

load("xl")
load("spectrum-mpi")
load("lsf-tools")
-- try_load("darshan-runtime/3.3.0-lite")
-- load("xalt")
