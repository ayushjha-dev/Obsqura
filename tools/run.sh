#!/usr/bin/env bash
#
# Run jekyll serve and then launch the site

prod=false
host="127.0.0.1"

help() {
  echo "Usage:"
  echo
  echo "   bash /path/to/run [options]"
  echo
  echo "Options:"
  echo "     -H, --host [HOST]    Host to bind to."
  echo "     -p, --production     Run Jekyll in 'production' mode."
  echo "     -h, --help           Print this help information."
}

while (($#)); do
  opt="$1"
  case $opt in
  -H | --host)
    host="$2"
    shift 2
    ;;
  -p | --production)
    prod=true
    shift
    ;;
  -h | --help)
    help
    exit 0
    ;;
  *)
    echo -e "> Unknown option: '$opt'\n"
    help
    exit 1
    ;;
  esac
done

if ! [[ $host =~ ^[A-Za-z0-9._:-]+$ ]]; then
  echo "> Invalid host value: '$host'"
  exit 1
fi

command=(bundle exec jekyll s -l -H "$host")

if [ -e /proc/1/cgroup ] && grep -q docker /proc/1/cgroup; then
  command+=(--force_polling)
fi

echo
printf '> '
if $prod; then
  printf 'JEKYLL_ENV=production '
fi
printf '%q ' "${command[@]}"
echo
echo

if $prod; then
  JEKYLL_ENV=production "${command[@]}"
else
  "${command[@]}"
fi
