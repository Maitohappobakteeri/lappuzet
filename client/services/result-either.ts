enum ResultEitherType {
  RESULT,
  ERROR,
}

export class ResultEither<R, E> {
  constructor(private type: ResultEitherType, private value: R | E) {}

  getOrCallable<D>(ifError: () => D): R | D {
    return this.isResult() ? (this.value as R) : ifError();
  }

  getOrValue<D>(ifError: D): R | D {
    return this.isResult() ? (this.value as R) : ifError;
  }

  whenResult(callable: (e: R) => void): boolean {
    if (!this.isError()) {
      callable(this.value as R);
      return true;
    }

    return false;
  }

  whenError(callable: (e: E) => void): boolean {
    if (this.isError()) {
      callable(this.value as E);
      return true;
    }

    return false;
  }

  map<M>(operation: (r: R) => M): ResultEither<M, E> {
    if (this.isError()) {
      return ResultEither.error(this.value as E);
    }

    const result = this.value as R;
    return ResultEither.result(operation(result));
  }

  isResult(): boolean {
    return this.type === ResultEitherType.RESULT;
  }

  isError(): boolean {
    return this.type === ResultEitherType.ERROR;
  }

  static result<R, E>(result: R): ResultEither<R, E> {
    return new ResultEither<R, E>(ResultEitherType.RESULT, result);
  }

  static error<R, E>(error: E): ResultEither<R, E> {
    return new ResultEither<R, E>(ResultEitherType.ERROR, error);
  }
}
