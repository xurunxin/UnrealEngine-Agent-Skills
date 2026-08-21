# Reflection Checklist

## Header/UHT

- generated include is last;
- matching `GENERATED_BODY()` is present;
- reflected enum/struct/class names and specifiers are valid;
- module API macro is on cross-module public types;
- no unsupported template/reflected parameter type;
- metadata string and category syntax are well formed.

## Property contract

- ownership and GC visibility;
- edit/default/instance visibility;
- Blueprint read/write intent;
- transient/save/config/replication intent;
- asset loading strategy (hard vs soft reference);
- rename/type-change migration path.

## Function contract

- WorldContext/DefaultToSelf/AutoCreateRefTerm only when semantically correct;
- pure functions are cheap and side-effect free;
- network RPC has authority/validation behavior defined;
- events have stable signatures and sensible override policy;
- latent/async APIs define cancellation and completion exactly once.

## Rebuild

A successful Live Coding patch does not prove new reflected declarations are integrated. After changing reflected shape, perform a full build with Editor closed and reload affected assets.
