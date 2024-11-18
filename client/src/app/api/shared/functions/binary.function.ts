export function convertFromStringToBuffer(value: string): Uint8Array {
  const jsonString = typeof value === 'string' ? value : JSON.stringify(value);
  const encoder = new TextEncoder();
  return encoder.encode(jsonString);
}
