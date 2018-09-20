export function parseUrl(url){
  const parser = document.createElement('a');
  parser.href = url;

  const info = {};
  const props = 'protocol hostname host pathname origin port search hash href'.split(' ');
  for (let prop of props){
    if (prop in parser){
      info[prop] = parser[prop];
    }
  }
  const query = parser.search.substring(1).split('&');
  info.query = {};
  for (let part of query) {
    if (part === '') // check for trailing & with no param
      continue;
    const param = part.split('=');
    info.query[decodeURIComponent(param[0])] = decodeURIComponent(param[1] || '');
  }
  return info;
}

export function fileSize(file){
  if (!file || file.size == 0){
    return '0 KB'
  }

  switch (true) {
    case file.size <= 1024:
      return '1 KB'
      //break;
    case file.size > 1024 && file.size <= 1048576:
      return Math.round(file.size/1024, 1) + ' KB';

    case file.size > 1048576 && file.size <= 1073741824:
      return Math.round(file.size/1048576, 1) + ' MB';

    case file.size > 1073741824 && file.size <= 1099511627776:
      return Math.round(file.size/1073741824, 1) + ' GB';

    case file.size >= 1099511627776:
      return Math.round(file.size/1099511627776, 1) + ' TB';

    default:
      return '0 KB'
  }
}