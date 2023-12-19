import psutil
cpu_stats = psutil.cpu_stats()

jsobj = {
    "ctx_switches":cpu_stats.ctx_switches,
    "interrupts":cpu_stats.interrupts,
    "soft_interrupts":cpu_stats.soft_interrupts,
    "syscalls":cpu_stats.syscalls
}

print(jsobj)