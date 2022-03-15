# telegram_event_notifier

A telegram bot which lets you setup notifications for the 42 intra-events

## Table of contents
1. [About](#about)
2. [MLX](#mlx)
3. [How to use](#howtouse)
4. [Leaks](#leaks)
5. [Protection](#protection)


## About

This project is a telegram bot that lets your interact with events from the intra.
As I have written this bot in about 3 days as a pyton-beginner my spaghetti-code is probably full of bad practices and
errors. During the project I also realized that my approach is far from perfect and therefor one of my [feature goals](#goals) is
to restructure the project

**features:**
- login with your intra
- setup notifications for events
- delete notifications
- get an icalander event to add to your calander
- no constant authorization needed (refreshes tokens automatically)

## Requirements

The basic python-bot runs in a docker container and therefore only needs docker. If you want to run the bot outside of a container you will
find the requirements in bot/requirements.txt and the source files in bot/src.
But because the bot needs an intra-authentication, which is send to the redirect-website via a query-parameters called *code* and telegram-bots
only accept query-parameters called *start* or *startgroup*, theres also a nginx server running. This nginx server simply redirects the request
to the telegram bot with the parameter *code* asigned to *start*.
To run both containers (nginx-servr and python-bot) the project uses docker-compose, but you can also run them seperately as they are not using
a docker-network.

## How to use

Clone the repo:
```bash

To use the library just compile it as if it was the real mlx-libray which means include mlx.h...
```c
#include "mlx/mlx.h" //adjust the path if you are using a different directory-structure
```
compile with the framework flags...:
```bash
cc -YOURFLAGS -framework OpenGL -framework AppKit -lmlx //adjust -lmlx if you are using a different directory-structure
```
if you are already using mlx you can just copy the mlx-folder out of this repository and use it the same was as the real mlx

## Leaks

For leaks the programm will show you all undestroyed images and windows when your programm exits (not if it gets signaled).
Be aware: not all leaks are gonna fail you if you submit your project but it won't harm your project if you fix them. 
Also if it doesnt print anything at exit, it doesn't mean your project doesn't have leaks. This library only checks for mlx-leaks,
meaning malloc or similar functions are not getting tracked.
Always check leaks for yourself and dont rely on this tool.

**mlx_init:**

the mlx_init function allocates memory in a struct, but there is not function to properly free everything mlx_init allocated. If you tried fixing this by
simply freeing the mlx_ptr, you probably realized that there are still leaks. That is the case because the mlx_ptr is a pointer to a struct which contains a pointer to an allocated image. 
This library contains a mlx_destroy function to fix this leak. If you don't wanna submit your project with this library, you can copy following code into your mlx_library:

copy the prototype in mlx.h:
```c
void	mlx_destroy(void *mlx_ptr);
```
copy the function in mlx_init_loop.m:
```c
void	mlx_destroy(void *mlx_ptr)
{
	mlx_ptr_t	*ptr;

	ptr = mlx_ptr;
	mlx_destroy_image(ptr, ptr->font);
	free(ptr);
}
```

## Protection

This is a second feature this library supports. You can check if your protection guards work properly.
To use it compile the library like this:
```bash
export PROTECTION_VALUE=X; make --directory=PATHTOMLX
```
replace X with the number of the protection you want to check (0 being the first).
What does this mean? :
if you compile with a PROTECTION_VALUE >= 0 it means that the library is gonna return NULL on the
X-th call of a mlx-create function.
