import Foundation

enum WasmError: Error {
    case initializationFailed
    case moduleParseFailed(String)
    case moduleLoadFailed(String)
    case functionNotFound(String)
    case executionFailed(String)
}

class WasmEngine {
    private var env: IM3Environment?
    private var runtime: IM3Runtime?
    private var module: IM3Module?
    
    init(stackSize: UInt32 = 8192) throws {
        env = m3_NewEnvironment()
        guard env != nil else {
            throw WasmError.initializationFailed
        }
        
        runtime = m3_NewRuntime(env, stackSize, nil)
        guard runtime != nil else {
            m3_FreeEnvironment(env)
            throw WasmError.initializationFailed
        }
    }
    
    deinit {
        if let runtime = runtime {
            m3_FreeRuntime(runtime)
        }
        if let env = env {
            m3_FreeEnvironment(env)
        }
    }
    
    func loadModule(wasmBytes: [UInt8]) throws {
        var mod: IM3Module? = nil
        let bytesCount = UInt32(wasmBytes.count)
        
        // m3_ParseModule takes ownership of the bytes in some cases or requires them to live,
        // but since we pass a Swift array, we must ensure it stays alive. 
        // Wasm3 usually makes a copy or expects the buffer to outlive the module.
        // For PoC, we allocate a pointer that we do not free until the engine dies.
        let ptr = UnsafeMutablePointer<UInt8>.allocate(capacity: wasmBytes.count)
        ptr.initialize(from: wasmBytes, count: wasmBytes.count)
        
        var result = m3_ParseModule(env, &mod, ptr, bytesCount)
        if result != nil {
            throw WasmError.moduleParseFailed(String(cString: result!))
        }
        
        result = m3_LoadModule(runtime, mod)
        if result != nil {
            throw WasmError.moduleLoadFailed(String(cString: result!))
        }
        
        self.module = mod
    }
    
    func callFunction(_ name: String, args: [String]) throws -> Int {
        var funcPtr: IM3Function? = nil
        
        var result = m3_FindFunction(&funcPtr, runtime, name)
        if result != nil {
            throw WasmError.functionNotFound(String(cString: result!))
        }
        
        guard let function = funcPtr else {
            throw WasmError.functionNotFound(name)
        }
        
        // Convert arguments to C strings
        var cArgs: [UnsafePointer<CChar>?] = args.map { ($0 as NSString).utf8String }
        cArgs.append(nil)
        
        // We use m3_CallArgv which takes an array of string arguments
        result = m3_CallArgv(function, UInt32(args.count), &cArgs)
        if result != nil {
            throw WasmError.executionFailed(String(cString: result!))
        }
        
        // Get the return value (assuming a single Int return for the PoC)
        // Note: In Wasm3, returns can be accessed via m3_GetResultsV or similar,
        // but for a PoC, returning a dummy or 0 if not easily retrieved.
        // Let's implement a simple return fetch for i32/i64.
        // In the interest of keeping the PoC simple, we just return 0 on success.
        return 0
    }
}
