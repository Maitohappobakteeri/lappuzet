export function notNull<T>(value: T | null): value is T {
  return value !== null;
}

export function isNull<T>(value: T | null): value is null {
  return value === null;
}

export function notUndefined<T>(value: T | undefined): value is T {
  return value !== undefined;
}

export function isDefined<T>(value: T | undefined | null): value is T {
  return notNull(value) && notUndefined(value);
}
