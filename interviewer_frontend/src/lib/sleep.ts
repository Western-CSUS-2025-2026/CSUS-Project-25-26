/** Used to sleep for a specified number of ms, this is a dev tool for simulating network call times
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}
