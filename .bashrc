# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
[ -z "$PS1" ] && return

# don't put duplicate lines in the history. See bash(1) for more options
# ... or force ignoredups and ignorespace
HISTCONTROL=ignoredups:ignorespace

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "$debian_chroot" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes

if [ -n "$force_color_prompt" ]; then
    if [ -x /usr/bin/tput ] && tput setaf 1 >&/dev/null; then
	# We have color support; assume it's compliant with Ecma-48
	# (ISO/IEC-6429). (Lack of such support is extremely rare, and such
	# a case would tend to support setf rather than setaf.)
	color_prompt=yes
    else
	color_prompt=
    fi
fi

if [ "$color_prompt" = yes ]; then
    PS1='${debian_chroot:+($debian_chroot)}\[\033[01;32m\]\u@\h\[\033[00m\]:\[\033[01;34m\]\w\[\033[00m\]\$ '
else
    PS1='${debian_chroot:+($debian_chroot)}\u@\h:\w\$ '
fi
unset color_prompt force_color_prompt

# If this is an xterm set the title to user@host:dir
case "$TERM" in
xterm*|rxvt*)
    PS1="\[\e]0;${debian_chroot:+($debian_chroot)}\u@\h: \w\a\]$PS1"
    ;;
*)
    ;;
esac

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    test -r ~/.dircolors && eval "$(dircolors -b ~/.dircolors)" || eval "$(dircolors -b)"
    alias ls='ls --color=auto'
    #alias dir='dir --color=auto'
    #alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi

# some more ls aliases
alias ll='ls -alFhtr  --color=auto'
alias la='ls -A'
alias l='ls -CF'
alias SOFTWARE='cd /pub/SOFTWARE/'
alias DATABASE='cd /pub/Database/'
alias Script='cd /pub/SOFTWARE/Other/Script'
#alias R='R3.2'
# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
#if [ -f /etc/bash_completion ] && ! shopt -oq posix; then
#    . /etc/bash_completion
#fi


########################################################################
##############################spades####################################
#######################################################################
export PATH=$PATH:/pub/SOFTWARE/Assembly/SPAdes-3.1.0-Linux/bin

#############################gicl#########################################
export PATH=$PATH:/pub/SOFTWARE/Assembly/gicl
#########################pear###########################################
export PATH=$PATH:/pub/SOFTWARE/Assembly/pear-0.9.5-bin-64/
########################WGS#############################################
export PATH=$PATH://pub/SOFTWARE/Assembly/wgs-8.3rc2/Linux-amd64/bin
############################Script##################################
export PATH=$PATH:/pub/SOFTWARE/Other/Script
##################################Trinity##################################
export PATH=$PATH:/pub/SOFTWARE/Assembly/trinityrnaseq-2.0.2:/pub/SOFTWARE/Pacbio/smrtanalysis/install/smrtanalysis_2.3.0.140936/analysis/bin/gmap_home/bin/
export PATH=$PATH:/pub/SOFTWARE/Assembly/trinityrnaseq_r20140717/util:/pub/SOFTWARE/Assembly/trinityrnaseq_r20140717/trinity-plugins/transdecoder
export PATH=$PATH:/pub/SOFTWARE/Assembly/trinityrnaseq_r20140717/Analysis/DifferentialExpression
###################################iAssembler#################################
export PATH=$PATH:/pub/SOFTWARE/Assembly/iAssembler-v1.3.2.x64
export TimeOut=0
##################################Prokka###########################
export PATH=$PATH:/pub/SOFTWARE/Other/prokka-1.11/bin:/pub/SOFTWARE/Other/prokka-1.11/binaries/linux
########################Rnammer#################################################

export PATH=$PATH:/pub/SOFTWARE/Other/Rnammer
###########################aragon##########################################
export PATH=$PATH:/pub/SOFTWARE/Other/aragorn1.2.36/
#######################barrnap##############
export PATH=$PATH:/pub/SOFTWARE/Other/barrnap-0.4.2/bin
################signalip#######################
export PATH=$PATH:/pub/SOFTWARE/Other/signalp-4.1/
###################estscan###############################
export PATH=$PATH:/pub/SOFTWARE/Other/BTLib-2.0b/ESTScan:/pub/SOFTWARE/Assembly/Platanus

#####################Mummer#####################
export PATH=$PATH:/pub/SOFTWARE/Other/MUMmer3.23

##################inparanoid_4#####################
export PATH=$PATH:/pub/SOFTWARE/Other/inparanoid_4.1

###################Zipper############################
export PATH=$PATH:/home/lpp/Project/Zipper:/pub/SOFTWARE/Other/blat_binary
#################sra_tools##############################
export PATH=$PATH:/pub/SOFTWARE/Other/sratoolkit.2.3.2-5-ubuntu64/bin:/pub/SOFTWARE/Other/stampy-1.0.23
###################RECON##############################
export PATH=$PATH:/pub/SOFTWARE/Other/RECON-1.08/scripts/:/pub/SOFTWARE/Other/RECON-1.08/bin/
######################Repeatscout################################
export PATH=$PATH:/pub/SOFTWARE/Other/RepeatScout-1/
###################TRF#########################################
export PATH=$PATH:/pub/SOFTWARE/Other/TRF
##############RepeatMaksker############
export PATH=$PATH:/pub/SOFTWARE/Other/RepeatMasker

####################MicroBiologyPipe##############
export PATH=$PATH:/home/lpp/test/MicroBiologyPipeline:/usr/local/mysql/bin/
alias Pro="cd ~lpp/Project/"
alias Falcon="cd /home/lpp/Project/mianlingchong/EcTools/Falcon"
#alias RS_3.2="/pub/SOFTWARE/Other/R-3.2.0/bin/Rscript"
#alias R3.2="/pub/SOFTWARE/Other/R-3.2.0/bin/R"
#################ectools##################
export ECTOOLS_HOME=/pub/SOFTWARE/Pacbio/ectools-master

#################FONT#########################
export LC_CTYPE=en_US.UTF-8
export LC_ALL=en_US.UTF-8
######################lastz######################################
export PATH=$PATH:/pub/SOFTWARE/Other/lastz-distrib-1.03.46/src:/pub/SOFTWARE/Other/HaploMerger_20120810/chainNet_jksrc20100603_ubuntu64bit:/pub/SOFTWARE/Other/HaploMerger_20120810/bin:/pub/SOFTWARE/Other/PhageFinder/bin
export AUGUSTUS_CONFIG_PATH=/pub/SOFTWARE/Other/augustus-3.2.2/config/
###########################RepeatModler########
export PATH=$PATH:/pub/SOFTWARE/Other/RepeatModeler:/pub/SOFTWARE/Other/PASA_r20140417:/pub/SOFTWARE/Other/PASA_r20140417/seqclean/seqclean:/pub/SOFTWARE/Other/PASA/scripts/:/pub/SOFTWARE/Other/kobas2.0-20150126/scripts:/pub/SOFTWARE/Other/augustus-3.2.2/scripts/:/pub/SOFTWARE/Other/augustus-3.2.2/bin/:/pub/SOFTWARE/Other/bamtools/bin
export BAMTOOLS_PATH=/pub/SOFTWARE/Other/bamtools/bin
export PASAHOME=/pub/SOFTWARE/Other/PASA_r20140417
####################Augustus#########

export PATH=$PATH:/pub/SOFTWARE/Other/augustus-3.2.2/scripts:/pub/SOFTWARE/Assembly/kakitone-finishingTool-c6fc560:/pub/SOFTWARE/Other/PASA_r20140417/bin/:/pub/SOFTWARE/Other/sratoolkit.2.5.0-1-ubuntu64/bin:/pub/SOFTWARE/Other/RepeatModeler/:/pub/SOFTWARE/Other/proovread/bin:/pub/SOFTWARE/Other/samtools-1.2:/pub/SOFTWARE/Pacbio/DALIGNER/:/pub/SOFTWARE/Pacbio/DAZZ_DB/:/pub/SOFTWARE/Other/BRAKER:/pub/SOFTWARE/Other/STAR/STAR-STAR_2.4.2a/bin/Linux_x86_64:/pub/SOFTWARE/Other/ghostz-1.0.0

export kobas_home=/pub/SOFTWARE/Other/kobas2.0-20150126/
export PYTHONPATH=PYTHONPATH:/pub/SOFTWARE/Other/kobas2.0-20150126/src
#########ICORN@##########################
export ICORN2_THREADS=64
export ICORN2_HOME=/pub/SOFTWARE/Other/ICORN2/
#####################EVM#######################
export  EVM_HOME=/pub/SOFTWARE/Other/EVM_r2012-06-25/
export AUGUSTUS_CONFIG_PATH=/pub/SOFTWARE/Other/augustus-3.2.2/config
export GENEMARK_PATH=/pub/SOFTWARE/Other/Genmarks/gm_et_linux_64/gmes_petap/
export SEYMOUR_HOME=/pub/SOFTWARE/Pacbio/smrtanalysis/install/smrtanalysis_2.3.0.140936/
export LD_LIBRARY_PATH=/pub/SOFTWARE/Other/boost$LD_LIBRARY_PATH
export PATH=$PATH:/pub/SOFTWARE/Other/Bridger_r2014-12-01:/pub/SOFTWARE/Other/aragorn1.2.36
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/jre/
export CLASSPATH=$JAVA_HOME/bin
export PERl5LIB=$PERl5LIB:/pub/SOFTWARE/Other/tRNAscan-SE-1.3.1/
export PERLLIB=$PERLLIB:/pub/SOFTWARE/Other/tRNAscan-SE-1.3.1/:/pub/SOFTWARE/Other/PhageFinder/lib:/pub/SOFTWARE/Other/PGAP-1.12
export PATH=$PATH:/pub/SOFTWARE/Other/PGAP-1.2.1:/pub/SOFTWARE/Other/Script/total/Script/:/pub/SOFTWARE/Other/HaploMerger_20120810/bin/:/pub/SOFTWARE/Other/tRNAscan-SE-1.3.1:/pub/SOFTWARE/Other/barrnap-0.4.2/bin:/pub/SOFTWARE/Other/pilercr:/pub/SOFTWARE/Other/Script/AnnoPipe:/pub/SOFTWARE/Other/Rnammer:/pub/SOFTWARE/Other/diamond/bin:/pub/SOFTWARE/Other/blastall/blast-2.2.17/bin:/pub/SOFTWARE/Other/prokka-1.11/bin:/pub/SOFTWARE/Other/GIHunter:/usr/share/samtools/:/pub/SOFTWARE/Assembly/EdenaV3.131028/bin:/usr/bin/:/pub/SOFTWARE/Other/PhageFinder_2.1/phage_finder_v2.1/bin/:/pub/SOFTWARE/Scaffolding/amos/bin/:/pub/SOFTWARE/Other/PGAP-1.12:/pub/SOFTWARE/Other/NovoAligner/novocraft:/pub/SOFTWARE/Other/gview/:/pub/SOFTWARE/Assembly/SPAdes-3.7.1-Linux/bin:/pub/SOFTWARE/Other/SSPACE-STANDARD-3.0_linux-x86_64:/pub/SOFTWARE/Transcriptome_Assembly/stringtie-1.2.2.Linux_x86_64:/pub/SOFTWARE/Other/bedops/applications/bed/conversion/bin:/pub/SOFTWARE/Other/bedops/applications/bed/conversion/src/wrappers:/pub/SOFTWARE/Other/bedops/bin:/pub/SOFTWARE/Other/subread-1.5.0-p2-Linux-x86_64/bin:/pub/SOFTWARE/Other/PASA_r20140417/misc_utilities:/pub/SOFTWARE/Other/Genmarks/gm_et_linux_64/gmes_petap:/pub/SOFTWARE/Other/maker/bin
export DISPLAY=:0
ulimit -SHn 40960
CLASSPATH=$CLASSPATH:/pub/SOFTWARE/Other/gview/gview.jar
#source activate LPP
MicroPipe=`python -c "from MicroPipe.Scripts import __path__ as path; print(path[0])"`
export PATH=$PATH:$MicroPipe:/pub/SOFTWARE/Assembly/MaSuRCA-3.2.1_08102016/bin
