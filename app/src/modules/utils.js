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