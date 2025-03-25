# Artifacts SDK

## Overview

A wrapper around the Artifacts API with some conveniences. Including automatic caching, throttling requests to stay within rate limits, and awaiting cooldowns. I've chosen a synchronous programming style, sacrificing some flexibility in exchange for simplicity. This means no task queue. Check out `main.py` for some sample code.

## Setup
- fork the code
- `pip install -e .`
- copy `.env.template` to `.env` and paste your API token into it
- get coding!

## SDK Hierarchy

The lowest level modules exist in the `utils` dir. Above that in the hierarchy is the `macros` dir, then `tactics`, then `strategies`, and finally your main entry point (or at least mine) is `main.py`.

This design is intended to allow for enough layers of abstraction to stay organized. It would be an anti-pattern to import modules from a higher level into modules of a lower level. To be really pedantic, it's an anti-pattern to import modules of the same hierarchical level into one another, one which I've already (carefully) violated myself, but I suggest not following my example and being more strict as you add more code to your fork.

If two methods seem more or less interchangeable, always use the **higher level** one, unless there's a good reason not to (it probably exists for a reason, and that reason is usually to manage/leverage state and/or to limit network calls).

### What you'll find in `./utils`

- `./utils/api.py`: Lowest level wrapper of Artifacts API endpoints.
- `./utils/constants.py`: Self explanatory.
- `./utils/cooldown_controller.py`: Where you'll find the logic behind cooldown and rate limit management. Automatically segregated by character.
- `./utils/state.py`: Not that much! Basically for the constants that need to change during runtime. Automatically segregated by character.
- `./utils/websocket_subscriptions.py`: WS boilerplate.

### What you'll find in `./macros`

- `./macros/find_monsters.py`: The easiest way to find monsters on the map meeting some criteria.
- `./macros/get_all.py`: Higher level API wrapper that returns a list (unpaginated) of the entire glossary of a specific type of thing. Automatically cached when possible
- `./macros/get_one.py`: Higher level API wrapper that returns a single specific instance of a specific type of thing. Automatically cached when possible
- `./macros/repeat.py`: The laziest way to keep doing something. Give it a function (and an optional number of iterations), it'll repeat it until it returns a truthy value or until your max iterations is reached, whichever comes first.
- `./macros/choose_your_character.py`: Changes which character is currently active. Influences state.
- `./macros/safe_move.py`: Doesn't move if the current character is already at the destination. Influences state.

### What you'll find in `./tactics`

- `./tactics/sim_battle.py`: For all your battle simulation needs. Currently the highest level (and probably most useful) method in this modules are `simulate_battles`, which returns statistics about a character's likelihood of success against any given monster. It does simulate effects and utilities. And, `get_character_battle_stats`, which generates one of the inputs for the aforementioned.

### What you'll find in `./strategies`

- Nothing, this is your work 😊

# Known issues/shortcomings

- Limited functionality. In it's current state this, is pretty bare bones. I just started...
- No retry logic. The lowest level wrapper throws exceptions when errors are returned, but it's up to you to decide what to do with them.
- Websockets are under developed. I wasn't commensurately thorough or opinionated about this as I was the rest of what I wrote. That leaves this functionality feeling aimless. My suggestion might be to have WS hooks update state. This could cascade into certain strategies kicking off, or something...
- Not every endpoint of the Artifacts API is wrapped. Notably account management such as creating an account, changing a password, and creating a new API token, are missing.
- Cached data never expires. That means it could roll over from one season to the next or between patches and include wrong information. **To clear your cached data just delete the `.json` files in the `./cached_data` dir**
- Multiple machines on same IP will run into each other's rate limits (deal with it).
- No tests yet.

The above list isn't exhaustive, please help me improve it.

**Suggestions and PRs are welcome, submit issues as much as you like, I'm not guaranteeing my continued involvement with the project**

Overall, a pretty compelling endorsement for an library right?!