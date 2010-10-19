import SCons.cpp

# component options

# make all component false
RT_USING_FINSH 		= False
RT_USING_DFS 		= False
RT_USING_DFS_ELMFAT = False
RT_USING_DFS_YAFFS2	= False
RT_USING_LWIP 		= False
RT_USING_WEBSERVER	= False
RT_USING_RTGUI 		= False
RT_USING_MODULE		= False

# parse rtconfig.h to get used component
PreProcessor = SCons.cpp.PreProcessor()
f = file('rtconfig.h', 'r')
contents = f.read()
f.close()
PreProcessor.process_contents(contents)
rtconfig_ns = PreProcessor.cpp_namespace

# finsh shell options
if rtconfig_ns.has_key('RT_USING_FINSH'):
	RT_USING_FINSH = True

# device virtual filesystem options
if rtconfig_ns.has_key('RT_USING_DFS'):
    RT_USING_DFS = True

    if rtconfig_ns.has_key('RT_USING_DFS_ELMFAT'):
        RT_USING_DFS_ELMFAT = True
    if rtconfig_ns.has_key('RT_USING_DFS_YAFFS2'):
        RT_USING_DFS_YAFFS2 = True

# lwip options
if rtconfig_ns.has_key('RT_USING_LWIP'):
    RT_USING_LWIP = True
    if rtconfig_ns.has_key('RT_USING_WEBSERVER'):
        RT_USING_WEBSERVER = True

# rtgui options
if rtconfig_ns.has_key('RT_USING_RTGUI'):
    RT_USING_RTGUI = True

# module options
if rtconfig_ns.has_key('RT_USING_MODULE'):
    RT_USING_MODULE = True

# CPU options
ARCH='mips'
CPU ='loongson'

# toolchains options
CROSS_TOOL  = 'gcc'
PLATFORM 	= 'gcc'
EXEC_PATH 	= 'E:/Program Files/CodeSourcery/Sourcery G++ Lite/bin'
BUILD		= 'debug'

PREFIX = 'mips-sde-elf-'
CC = PREFIX + 'gcc'
AS = PREFIX + 'gcc'
AR = PREFIX + 'ar'
LINK = PREFIX + 'gcc'
TARGET_EXT = 'elf'
SIZE = PREFIX + 'size'
OBJDUMP = PREFIX + 'objdump'
OBJCPY = PREFIX + 'objcopy'
READELF = PREFIX + 'readelf'

DEVICE = ' -mips2'
CFLAGS = DEVICE + ' -EL -G0 -DRT_USING_MINILIBC -mno-abicalls -fno-pic -fno-builtin -fno-exceptions -ffunction-sections -fomit-frame-pointer'
AFLAGS = ' -c' + DEVICE + ' -EL -fno-pic -fno-builtin -mno-abicalls -x assembler-with-cpp'
LFLAGS = DEVICE + ' -EL -Wl,--gc-sections,-Map=rtthread-3210.map,-cref,-u,Reset_Handler -T dev3210_ram.lds'

CPATH = ''
LPATH = ''

if BUILD == 'debug':
	CFLAGS += ' -O0 -gdwarf-2'
	AFLAGS += ' -gdwarf-2'
else:
	CFLAGS += ' -O2'

RT_USING_MINILIBC = True
DUMP_ACTION = OBJDUMP + ' -D -S $TARGET > rtt.asm\n'
READELF_ACTION = READELF + ' -a $TARGET > rtt.map\n'
POST_ACTION = OBJCPY + ' -O binary $TARGET rtthread.bin\n' + SIZE + ' $TARGET \n' + READELF_ACTION