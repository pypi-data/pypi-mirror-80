
    // Hook functions must be of this type
    typedef bool (*hook_func_t)(CPUState *, TranslationBlock *);

    void add_hook(target_ulong addr, hook_func_t hook);
    void update_hook(hook_func_t hook, target_ulong value);
    void enable_hook(hook_func_t hook, target_ulong value);
    void disable_hook(hook_func_t hook);

