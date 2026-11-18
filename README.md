# Demo-3d
Independent demo repository for [Group-Internship](https://github.com/STERILITZIA02/Group-Internship).

## Pitch 778 slide inserts

The six [1920 × 1080 PNGs](prototypes/pitch-778/) fit the 1344 × 756 image frames
on slides 5–7 and 13–15. Each comparison uses one fixed orthographic camera.

| Brief | Reference layout | Option A | Option B |
| --- | --- | --- | --- |
| 08 · Kitchen | [Measured room](prototypes/pitch-778/K1-measured.png) | [Wide island](prototypes/pitch-778/K2-wide-open.png) | [Narrow island](prototypes/pitch-778/K3-narrow-open.png) |
| 09 · Garden | [Yard and routes](prototypes/pitch-778/G1-yard.png) | [Tree beside table](prototypes/pitch-778/G2-table.png) | [Tree beside fence](prototypes/pitch-778/G3-fence.png) |

The kitchen wall measures 8.4 m in the demonstration model. Reducing the island
depth from 1,050 to 750 mm removes the shallow drawer bank. The open dishwasher
projects 600 mm into an aisle of 1,050 or 1,350 mm, leaving 450 or 750 mm clear.
The two figures illustrate the dinner task. Test the preferred option at full
scale with the household before requesting a quote.

Garden coordinates use metres east and north on level ground. Astral calculates
the solar direction for central Auckland (36.85° S, 174.76° E) on 15 January 2027
at 18:00 NZDT. Mitsuba casts shadows from the scene geometry using that
direction. Both options use the same illustrative mature canopy. The 460 mm
radius tree pit at site B leaves 630 mm to the fence for the 540 mm wide bin.
Hose lengths follow the drawn route from the tap via the bed to each tree.

With the dependencies below installed, run
`python prototypes/scenes/render_pitch.py --samples 60` to regenerate the inserts.

## Early spatial studies

Six low-fidelity 3D views explore two candidate project briefs. Read each row
from left to right. Open an image to inspect the model and its plan at full size.

### 08 · Kitchen design and visualisation

| Lay out the kitchen | Open the dishwasher | Try a slimmer island |
| --- | --- | --- |
| [![Cutaway kitchen with the island in place](prototypes/views/kitchen-01.png)](prototypes/views/kitchen-01.png) | [![Open dishwasher with a 32 cm gap to the island](prototypes/views/kitchen-02.png)](prototypes/views/kitchen-02.png) | [![Shorter island depth leaves an 87 cm gap](prototypes/views/kitchen-03.png)](prototypes/views/kitchen-03.png) |

The rear cabinets and the island's seating edge stay in place. Pulling its worktop
back by 55 cm gives the cook that much more room to pass the open dishwasher.
The dimensions describe this model.

### 09 · Landscape and garden planning

| Lay out the garden | Move the tree | Preview the canopy |
| --- | --- | --- |
| [![Sapling beside the raised strawberry bed](prototypes/views/garden-01.png)](prototypes/views/garden-01.png) | [![Sapling moved towards the deck, with its previous site marked](prototypes/views/garden-02.png)](prototypes/views/garden-02.png) | [![Larger crown at the same site, with the dining deck and gate route visible](prototypes/views/garden-03.png)](prototypes/views/garden-03.png) |

Follow the same tree from the strawberry bed to the deck, then compare its
grown crown under the same light. Growth and shadows illustrate the design
decision; species, season and site-specific sun angles are still open.

### Render the studies

The editable [scene models](prototypes/scenes/) use metres, with Z up. From
the demo root, run the following in a Python 3.12 virtual environment:

```sh
python -m pip install -r prototypes/requirements.txt
python prototypes/scenes/render.py
```

To render a single state, add `--theme kitchen --step 2` or
`--theme garden --step 3`. The image sheets use a fixed camera per brief.
An interactive application and its technology stack are still to be agreed.

## Setup placeholders

| Item | Value |
| --- | --- |
| Demo objective and audience | Help the internship team compare kitchen circulation and garden planting layouts |
| Scope and acceptance criteria | To be agreed |
| Stack and dependencies | To be chosen |
| Install / run / build commands | To be added |
| Tests and verification | To be added |
| Preview / deployment URL | To be added if needed |
| Version | To be set by the project owner |

## Working on this demo

Plan work on the [main Sprint board](https://github.com/users/STERILITZIA02/projects/2).
Create a task branch here and reference the main planning issue in the PR.
After merging, update this demo's submodule reference in the main repository.
See the [workflow guide](https://github.com/STERILITZIA02/Group-Internship/blob/main/docs/sprint-workflow.md).

The current Repository checks workflow only checks whitespace and checkout;
application checks will be added with the chosen stack.

All rights reserved. See [LICENSE](LICENSE).
