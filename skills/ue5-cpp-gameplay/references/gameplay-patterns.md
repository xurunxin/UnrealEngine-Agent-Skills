# Gameplay C++ Pattern Notes

## Lifecycle questions

- Is there a valid World at this callback?
- Does this run on CDO, archetype, preview world, PIE, server, client, or editor utility world?
- Who unregisters delegates/timers/async callbacks?
- What happens during seamless travel, map change, hot reload, or subsystem deinitialize?

## Reference selection

| Need | Prefer |
|---|---|
| Reflected owning UObject field | `UPROPERTY` + `TObjectPtr<T>` |
| Non-owning UObject that may disappear | `TWeakObjectPtr<T>` |
| Asset not necessarily loaded | `TSoftObjectPtr<T>` / `TSoftClassPtr<T>` |
| Class constrained by base | `TSubclassOf<T>` |
| Non-UObject unique ownership | `TUniquePtr<T>` |
| Shared non-UObject service | `TSharedPtr<T>` with explicit threading mode |

## Async checklist

Copy only value/thread-safe data into workers. Never assume a `TWeakObjectPtr` that was valid before scheduling remains valid. Marshal completion to Game Thread, recheck cancellation and object/world lifetime, then mutate UObject state.

## Tick alternatives

Delegate/event, timer, latent/async completion, subsystem batch, animation/physics callback, or explicit dirty queue. Measure before converting Tick to a more complex scheduler.
