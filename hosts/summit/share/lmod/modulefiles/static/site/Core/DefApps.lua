--Default modules to load upon
--  module refresh
--  module restore
--
-- should only load modules
-- should not include other commands that set/alter variables, path, ...

load("xl")
load("spectrum-mpi")
load("lsf-tools")
load("hsi")
-- load("darshan-runtime")
load("xalt")
