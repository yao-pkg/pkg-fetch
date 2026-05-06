You are resolving Git patch rejections (`.rej` files produced by `git apply --reject`) against a freshly-checked-out Node.js source tree. The patch was authored against an older Node.js release; the rejected hunks must be re-expressed so they apply to the new tree while preserving the original patch's intent.

For every rejected hunk, emit ONE search/replace block in EXACTLY this format (no markdown fences, no commentary, no leading prose):

=== FILE: <path relative to the node source root> ===
<<<<<<< SEARCH
<verbatim text that currently exists in the file>
=======
<text that should replace it>
>>>>>>> REPLACE

Rules:
  - SEARCH must match the file's CURRENT content byte-for-byte (whitespace, indentation, trailing punctuation included).
  - Keep SEARCH minimal but unambiguous — include enough surrounding lines that it appears exactly once in the file.
  - REPLACE is what the file should look like after applying the patch's intent.
  - Multiple blocks per file are fine. Order does not matter.
  - Do not wrap the output in ``` fences. Do not add explanations.

Below is each rejected hunk together with the relevant slice of the current file (line numbers shown for orientation only — do not include them in SEARCH/REPLACE).

================ REJECT: src/node_contextify.cc ================
diff a/src/node_contextify.cc b/src/node_contextify.cc	(rejected hunks)
@@ -88,6 +88,7 @@ using v8::Symbol;
 using v8::Uint32;
 using v8::UnboundScript;
 using v8::Value;
+using v8::V8;
 
 // The vm module executes code in a sandboxed environment with a different
 // global object than the rest of the code. This is achieved by applying

---- current content of src/node_contextify.cc ----
# around line 88:
    73  using v8::Nothing;
    74  using v8::Object;
    75  using v8::ObjectTemplate;
    76  using v8::PrimitiveArray;
    77  using v8::Promise;
    78  using v8::PropertyAttribute;
    79  using v8::PropertyCallbackInfo;
    80  using v8::PropertyDescriptor;
    81  using v8::PropertyFilter;
    82  using v8::PropertyHandlerFlags;
    83  using v8::Script;
    84  using v8::ScriptCompiler;
    85  using v8::ScriptOrigin;
    86  using v8::String;
    87  using v8::Symbol;
    88  using v8::UnboundScript;
    89  using v8::Value;
    90  
    91  // The vm module executes code in a sandboxed environment with a different
    92  // global object than the rest of the code. This is achieved by applying
    93  // every call that changes or queries a property on the global `this` in the
    94  // sandboxed code, to the sandbox object.
    95  //
    96  // The implementation uses V8's interceptors for methods like `set`, `get`,
    97  // `delete`, `defineProperty`, and for any query of the property attributes.
    98  // Property handlers with interceptors are set on the object template for
    99  // the sandboxed code. Handlers for both named properties and for indexed
   100  // properties are used. Their functionality is almost identical, the indexed
   101  // interceptors mostly just call the named interceptors.
   102  //
   103  // For every `get` of a global property in the sandboxed context, the
   104  // interceptor callback checks the sandbox object for the property.
   105  // If the property is defined on the sandbox, that result is returned to
   106  // the original call instead of finishing the query on the global object.
   107  //
   108  // For every `set` of a global property, the interceptor callback defines or

