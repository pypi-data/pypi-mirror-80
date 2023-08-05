
// returns minimal handles for processes in an array
GArray *get_process_handles(CPUState *cpu);

// returns the current thread
OsiThread *get_current_thread(CPUState *cpu);

// returns information about the modules loaded by the guest OS kernel
GArray *get_modules(CPUState *cpu);

// returns information about the memory mappings of libraries loaded by a guest OS process
GArray *get_mappings(CPUState *cpu, OsiProc *p);

// returns operating system introspection info for each process in an array
GArray *get_processes(CPUState *cpu);

// gets the currently running process
OsiProc *get_current_process(CPUState *cpu);

OsiModule* get_one_module(GArray *osimodules, unsigned int idx);

OsiProc* get_one_proc(GArray *osiprocs, unsigned int idx);

void cleanup_garray(GArray *g);

