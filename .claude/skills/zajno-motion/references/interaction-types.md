# Interaction Types — Real-time vs Not-real-time

Zajno's vocabulary for *when* an animation responds to user input.

## Real-time

Animation runs **during** the input. Every frame, the animation reads
the current input state.

Examples:
- Cursor-follower (cursor moves → element tracks it)
- Hover tilt (pointer position drives `rotateX/Y`)
- Scroll parallax (`scrub: true` ScrollTrigger)
- Drag interactions (Matter.js, GSAP Draggable)

Implementation: bind to a continuous event (`mousemove`, `scroll`,
`pointermove`, `requestAnimationFrame`) and update transforms on each
tick. **Always smooth the response** with a short tween or lerp; raw
event values look jittery.

```js
let targetX = 0, targetY = 0, currentX = 0, currentY = 0;

document.addEventListener("mousemove", e => {
  targetX = e.clientX;
  targetY = e.clientY;
});

function tick() {
  currentX += (targetX - currentX) * 0.1;   // lerp toward target
  currentY += (targetY - currentY) * 0.1;
  cursor.style.transform = `translate(${currentX}px, ${currentY}px)`;
  requestAnimationFrame(tick);
}
tick();
```

The `0.1` lerp factor controls smoothness — lower = smoother but laggier.

## Not real-time

Animation runs **after** the input ends (or in response to a discrete event).

Examples:
- Click → modal opens with a fade+scale
- Scroll past threshold → reveal triggers and completes on its own
  (`scrub: false`)
- Form submit → button morphs to spinner to checkmark
- Page navigation → exit + enter animation choreography

Implementation: fire a tween or timeline on a discrete event
(`click`, `submit`, `intersection observer`, `routeChange`).

```js
btn.addEventListener("click", () => {
  gsap.timeline()
    .to(".modal-backdrop", { opacity: 1, duration: 0.3 })
    .from(".modal", { scale: 0.92, opacity: 0, duration: 0.5, ease: "power3.out" }, "<");
});
```

## Choosing between them

| Question                                          | Answer            |
|---------------------------------------------------|-------------------|
| Does the user expect *immediate* spatial feedback?| Real-time         |
| Is the input a discrete event (click, submit)?    | Not real-time     |
| Are you binding to scroll position?               | Either — use scrub=true for real-time, scrub=false for not |
| Is performance a concern?                         | Not real-time (cheaper) |
| Does the animation tell a story?                  | Not real-time     |

## Mixing both

Most polished sites use both. A landing page might:

1. **Not real-time**: scroll past threshold → headline reveals
2. **Real-time**: as user scrolls further → parallax layers move with scroll
3. **Real-time**: cursor moves → custom cursor tracks it
4. **Not real-time**: user clicks CTA → button morphs to confirmation

The trap is making everything real-time — it's expensive and exhausting
to look at. Reserve real-time for moments where the *spatial* connection
to input is the entire point.
