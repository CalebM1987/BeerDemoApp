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