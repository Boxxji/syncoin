// test_hash.c
// A simple WASM module with a single exported function

__attribute__((visibility("default")))
int test_hash() {
    return 42; // The answer to life, the universe, and everything
}
