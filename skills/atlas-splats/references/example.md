# Example run: a studio as splats

The request was "turn this into a 3D scene I can look around in", from one 16:9 image of a
potter's studio seen from its doorway: a work table with a wheel and unfired bowls in the middle
of the room, shelves of pots along the walls, a kiln in a corner, windows on the left.

These are the choices made for this scene. Another scene, or another reading of the request,
calls for different ones. The run used the CLI alone, with contact sheets at the check-ins.

## What posing returned

[`pose-request.json`](../assets/example/pose-request.json) is the request and
[`pose-result.json`](../assets/example/pose-result.json) the part of the saved result that
matters. The camera is 0.97 above the floor and tilted about 7 degrees down. `fx` is 762 on a
1280-wide grid, an 80 degree horizontal field of view.

Reading the depth file gave a typical (median) depth of 2.5. The door frame is 1.3 from the
camera, so the camera stands outside the room. Beyond the frame the room is about 4 wide and 4.4
deep. The work table sits just inside the door with open floor on both sides and behind it. The
image says nothing about the wall the door is in, or about what is behind the camera.

## Building the scene

Three rounds. Each is one request with depth, with every frame kept so far as context.

**Round 1: step into the room.** Three cameras on floor the photo showed as open, each looking
where the photo did not: left of the table looking across it at the right wall, right of the
table looking across it at the window wall, and behind the table looking into the back corner.
Each saw about half known surface. What came back: the shelves run the whole right wall to the
door, windows run the whole left wall, and the kiln and back corner are now seen from close up.

**Round 2: the far end, looking back.** Nothing so far showed the wall with the door in it. Three
cameras at the back of the room, in floor that round 1 had confirmed as open, looking back
toward the door from the middle, the left and the right. What came back: through the doorway
there is a large workshop hall with an open dark ceiling, strip lights and rows of shelving. The
model invented all of it, and views 4 and 5 agree on it.

View 6 did not agree. It showed the window wall running on past the door into the hall, where
view 4 shows a wall with shelves, and a grey exit door nobody else had seen. It was kept at
first, and a round built on it repeated the exit door and the missing wall. View 6 was dropped
and round 3 was generated again without it. A view that disagrees is cheapest to drop when it
arrives.

**Round 3: what round 2 left thin.** Four cameras: beside the table on each side, looking at the
corners either side of the door; near the back, looking at the door's left side from a spot that
overlaps view 4 (it saw 82% known surface, where view 6's camera had seen 27%); and beside the
source camera, for a second look at the door frame, which only the source image had seen.

[`round-2-request.json`](../assets/example/round-2-request.json) is a whole round's request: the
four frames so far as context, three cameras, and `"returnDepth": true`.
[`round-1-request.json`](../assets/example/round-1-request.json) and
[`round-3-request.json`](../assets/example/round-3-request.json) are the others. The rounds took
18, 30 and 26 seconds and cost 70, 70 and 80 credits.

[`views.jpg`](../assets/example/views.jpg) shows the source image and all ten views by round.
The table, wheel, bowls, kiln and shelves keep their shape and place throughout.

## What the person saw

The contact sheet, with three notes: everything through the doorway is invented; the floor
changes from dusty concrete to smooth grey at the door; and the corner to the left of the door is
the least settled part of the scene. Then the cost and time of the reconstruction, 5,000 credits
and 15 to 25 minutes. They agreed to continue.

## The reconstruction

The ten frames were checked as input: the floor, the table from every side, all four walls from
inside the room, and the hall through the doorway appear in at least one view; the table, wheel
and kiln agree across views; and every frame is 1280x720 with depth. Ten is near the low end for
a room. It was enough here because the room is small and the views surround its one large
object.

[`splats-request.json`](../assets/example/splats-request.json) is the request: the posed frame
and the nine views that were kept, each with its image, depth and camera. It was submitted once,
refined, and took 18 minutes.

## The result

One SPZ file with 2,000,000 splats, 32 MB, in the same world as the cameras that were sent.
[`splats.jpg`](../assets/example/splats.jpg) shows it rendered from eight positions it was not
given: in through the door, round behind the table, and back toward the doorway.

- Inside the room the scene is sharp and holds together from every side, including the door wall
  and the shelves beside it, which the photo never showed.
- From the source camera's own position (the first picture) the door frame and threshold are
  clean. They were close to the lens, and view 9 gave them a second look from beside the source
  camera. Surfaces that only one view sees at close range tend to reconstruct poorly.
- Looking out through the doorway (the last pictures), the hall is recognisable but soft, and
  the glass in its windows is smeared. Only four views saw it, all from inside the room. It is
  a backdrop for views from the room, not somewhere to walk into.
