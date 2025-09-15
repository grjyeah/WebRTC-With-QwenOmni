import 'dart:convert';

/// 科大讯飞工具类
class XfUtils {
  /// 将DateTime转换为RFC1123格式字符串
  static String toRfc1123String(DateTime date) {
    final weekday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][date.weekday % 7];
    final month = [
      'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
      'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ][date.month - 1];

    final formattedDate = '$weekday, ${date.day.toString().padLeft(2, '0')} $month ${date.year} '
        '${date.hour.toString().padLeft(2, '0')}:${date.minute.toString().padLeft(2, '0')}:${date.second.toString().padLeft(2, '0')} GMT';

    return formattedDate;
  }

  /// URL安全的Base64编码
  static String urlSafeBase64Encode(List<int> bytes) {
    return base64Encode(bytes)
        .replaceAll('+', '-')
        .replaceAll('/', '_')
        .replaceAll('=', '');
  }

  /// URL安全的Base64解码
  static List<int> urlSafeBase64Decode(String base64String) {
    final padding = '=' * (4 - (base64String.length % 4));
    final safeBase64 = base64String.replaceAll('-', '+').replaceAll('_', '/') + padding;
    return base64Decode(safeBase64);
  }
}