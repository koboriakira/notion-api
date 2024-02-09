/**
 * 引数をキャメルケースに変換する
 *
 * @format
 * @param text
 * @returns
 */
export const convertToCamelCase = (text: string): string => {
  return text
    .split("_")
    .map((word, index) =>
      index === 0 ? word : word.charAt(0).toUpperCase() + word.slice(1)
    )
    .join("");
};
