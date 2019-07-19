#!/usr/bin/env bash

set -o pipefail

declare -i curl_speed
declare -i curl_status
declare filepath="dists/Debian10.0/main/Contents-source.gz"
declare -a mirrors
declare top_mirror
declare -i top_speed=0

mirrors+=("http://ftp.us.debian.org/debian" "http://debian-archive.trafficmanager.net/debian")
mirrors+=("http://debian.cc.lehigh.edu/debian" "http://debian.csail.mit.edu/debian")
mirrors+=("http://debian.cs.binghamton.edu/debian" "http://debian.cse.msu.edu/debian")
mirrors+=("http://debian.ec.as6453.net/debian" "http://debian.gtisc.gatech.edu/debian")
mirrors+=("http://debian.mirror.constant.com/debian" "http://debian.mirrors.pair.com/debian")
mirrors+=("http://debian.osuosl.org/debian" "http://debian.uchicago.edu/debian")
mirrors+=("http://ftp.naz.com/debian" "http://ftp.utexas.edu/debian")
mirrors+=("http://mirror.cc.columbia.edu/debian" "http://mirror.cogentco.com/debian")
mirrors+=("http://mirror.keystealth.org/debian" "http://mirror.math.princeton.edu/pub/debian")
mirrors+=("http://mirrors.accretive-networks.net/debian" "http://mirrors.advancedhosters.com/debian")
mirrors+=("http://mirrors.bloomu.edu/debian" "http://mirrors.cat.pdx.edu/debian")
mirrors+=("http://mirrors.edge.kernel.org/debian" "http://mirrors.gigenet.com/debian")
mirrors+=("http://mirror.siena.edu/debian" "http://mirror.sjc02.svwh.net/debian")
mirrors+=("http://mirrors.lug.mtu.edu/debian" "http://mirrors.namecheap.com/debian")
mirrors+=("http://mirrors.ocf.berkeley.edu/debian" "http://mirrors.syringanetworks.net/debian")
mirrors+=("http://mirror.steadfast.net/debian" "http://mirrors.wikimedia.org/debian")
mirrors+=("http://mirrors.xmission.com/debian" "http://mirror.us.leaseweb.net/debian")
mirrors+=("http://mirror.us.oneandone.net/debian" "http://repo.ialab.dsu.edu/debian")
mirrors+=("http://www.gtlib.gatech.edu/debian")

humanize() {
    local -i value=$1

    value=$((${value} * 8))
    if [[ ${value} -lt 1024 ]]; then
        echo "${value} bit/sec"
        return 0
    elif [[ ${value} -lt 1048576 ]]; then
        echo "$((${value} / 1024)) kbit/sec"
    else
        echo "$((${value} / 1048576)) mbit/sec"
    fi
}

for mirror in "${mirrors[@]}"; do
    curl_speed=$(curl -s -o /dev/null -w "%{speed_download}\n" --connect-timeout 3 --max-time 60 ${mirror}/${filepath} | sed 's/\..*//')
    curl_status=${PIPESTATUS[0]}
    if [[ ${curl_status} -ne 0 ]]; then
        declare fail_message
        case ${curl_status} in
            6)
                fail_message="Unable to resolve host"
                ;;
            7)
                fail_message="Unable to connect"
                ;;
            23)
                fail_message="Write error"
                ;;
            26)
                fail_message="Read error"
                ;;
            28)
                fail_message="Timed out"
                ;;
            *)
                fail_message="Unexpected error"
                ;;
        esac
        echo "${mirror}: ${fail_message}" >&2
        continue
    fi

    echo "${mirror}: $(humanize ${curl_speed})" >&2
    if [[ ${curl_speed} -gt ${top_speed} ]]; then
        top_mirror="${mirror}"
        top_speed="${curl_speed}"
    fi
done
echo "Fastest Mirror: ${top_mirror} @ $(humanize ${top_speed})"
