export function isDefined<T>(obj: T | undefined | null): obj is T {
  return obj !== undefined && obj !== null;
}
