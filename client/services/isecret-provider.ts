export const InjSecretProvider = Symbol.for("ISecretProvider");

export interface ISecretProvider {
  secretToken(): string;
}
