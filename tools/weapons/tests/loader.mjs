// Maps the bare "@minecraft/server" specifier onto the local mock so the engine modules
// can be imported unchanged by Node.
const MOCK = new URL("./mock_server.mjs", import.meta.url).href;

export async function resolve(specifier, context, nextResolve) {
  if (specifier === "@minecraft/server") return { url: MOCK, shortCircuit: true };
  return nextResolve(specifier, context);
}
