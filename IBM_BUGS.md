In spectrum-mpi-10.3.1.2-20200121-*/include/mpi.h:268:

```c
#if (1 == SMPI_HAVE_PRAGMA_WEAK)
   /*   
                    
    * test_version() is put into user's object files as
    * a weak symbol, so users can use a utility such as
    * strings to see what SMPI version it was built with.
    */
  #if defined(c_plusplus) || defined(__cplusplus)
    extern "C"
    {    
  #endif
      #pragma weak smpi_built_against_version
      OMPI_DECLSPEC const char * smpi_built_against_version(void);
      OMPI_DECLSPEC const char * smpi_built_against_version(void) { return "SMPI_BUILT_AGAINST_VERSION=" SMPI_VERSION_STR; }
  #if defined(c_plusplus) || defined(__cplusplus)
    } /* extern "C" */
  #endif
#endif
```

first declaration of `OMPI_DECLSPEC const char * smpi_built_against_version(void);` is redundant and problematic.
