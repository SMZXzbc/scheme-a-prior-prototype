# Demonstrations: Radio Map Prior v2

This file provides few-shot examples for generating structured radio-map-oriented priors.

The goal is to guide GPT to generate JSON priors that are useful for downstream Radio Map / Pathloss Map / Channel Knowledge Map generation.

* * *

## Demonstration 1: Dense Urban + 28 GHz + Open Square LOS

### Input

    case_id: DU_006
    scene_type: dense urban
    frequency_GHz: 28
    condition: open square LOS

### Output
```json
    {
      "case_id": "DU_006",
      "scene_type": "dense urban",
      "frequency_GHz": 28,
      "condition": "open square LOS",
    
      "radio_map_task": "pathloss_map_generation",
    
      "dominant_mechanism": "LOS",
      "mechanism_weights": {
        "los": 0.55,
        "reflection": 0.30,
        "diffraction": 0.03,
        "scattering": 0.07,
        "penetration": 0.05
      },
    
      "pathloss_level_hint": "medium",
    
      "los_region_hint": "LOS regions are expected to dominate near the transmitter and across open square areas.",
      "nlos_region_hint": "NLOS regions are limited and mainly appear behind nearby buildings or obstacles around the square.",
      "shadowing_region_hint": "Weak to moderate shadowing may occur behind buildings, trees, or large objects near the square boundary.",
      "blockage_region_hint": "Nearby buildings, trees, and temporary obstacles may create local blockage, but the main open area remains mostly LOS.",
    
      "reflection_region_hint": "Reflections may occur from surrounding building facades, ground surfaces, and nearby walls.",
      "diffraction_region_hint": "Diffraction is weak at 28 GHz and may only occur around building edges near the square boundary.",
      "scattering_region_hint": "Scattering is limited but may come from rough ground, small objects, trees, and street furniture.",
    
      "building_density_hint": "medium",
      "material_hint": "Concrete, glass facades, and ground surfaces may provide secondary reflected paths in the open square environment.",
      "effective_scatterer_hint": "Surrounding building walls, ground surfaces, trees, and street furniture may act as effective scatterers.",
    
      "spatial_variation_hint": "Spatial variation is relatively smooth in the open LOS area but becomes stronger near buildings and shadow boundaries.",
      "map_pattern_hint": "The generated pathloss map should show relatively lower pathloss near the transmitter and open LOS regions, with localized higher pathloss behind buildings or obstacles.",
    
      "conditioning_summary": "For dense urban 28 GHz open square LOS radio map generation, the prior should emphasize LOS-dominant propagation, moderate pathloss, smooth spatial variation in open areas, and local shadowing near obstacles."
    }
```

## Demonstration 2: Dense Urban + 28 GHz + Narrow Street Canyon NLOS

### Input

    case_id: DU_011
    scene_type: dense urban
    frequency_GHz: 28
    condition: narrow street canyon NLOS

### Output
```json
    {
      "case_id": "DU_011",
      "scene_type": "dense urban",
      "frequency_GHz": 28,
      "condition": "narrow street canyon NLOS",
    
      "radio_map_task": "pathloss_map_generation",
    
      "dominant_mechanism": "reflection",
      "mechanism_weights": {
        "los": 0.03,
        "reflection": 0.65,
        "diffraction": 0.08,
        "scattering": 0.20,
        "penetration": 0.04
      },
    
      "pathloss_level_hint": "high",
    
      "los_region_hint": "LOS regions are very limited and may only exist near the transmitter or along short open street segments.",
      "nlos_region_hint": "Most receiver locations inside the narrow street canyon are likely to be NLOS, especially behind building corners.",
      "shadowing_region_hint": "Strong shadowing is expected behind dense buildings and around street corners where the direct path is blocked.",
      "blockage_region_hint": "Building blocks and street-canyon corners are the main blockage sources.",
    
      "reflection_region_hint": "Strong reflected components are likely along building facades, street canyon walls, and smooth vertical surfaces.",
      "diffraction_region_hint": "Diffraction may occur around building edges and corners, but its contribution is weak at 28 GHz.",
      "scattering_region_hint": "Moderate scattering may come from rough walls, street furniture, vehicles, and small objects inside the canyon.",
    
      "building_density_hint": "high",
      "material_hint": "Concrete and glass building facades are likely to dominate the propagation environment; glass surfaces may enhance specular reflection, while rough concrete may increase scattering.",
      "effective_scatterer_hint": "Nearby building walls, street corners, vehicles, and rough facade surfaces are likely effective scatterers.",
    
      "spatial_variation_hint": "Strong spatial variation with sharp pathloss changes near blockage boundaries and street corners.",
      "map_pattern_hint": "The generated pathloss map should show high pathloss in deep NLOS regions, relatively lower pathloss along reflection-supported street segments, and sharp transitions near building edges.",
    
      "conditioning_summary": "For dense urban 28 GHz narrow street canyon NLOS radio map generation, the prior should emphasize reflection-dominant propagation, high pathloss, limited LOS coverage, strong shadowing behind buildings, and sharp spatial variation near street corners."
    }

```
* * *

## Demonstration 3: Dense Urban + 28 GHz + Heavy Pedestrian Blockage

### Input

    case_id: DU_014
    scene_type: dense urban
    frequency_GHz: 28
    condition: heavy pedestrian blockage

### Output
```json
    {
      "case_id": "DU_014",
      "scene_type": "dense urban",
      "frequency_GHz": 28,
      "condition": "heavy pedestrian blockage",
    
      "radio_map_task": "pathloss_map_generation",
    
      "dominant_mechanism": "mixed",
      "mechanism_weights": {
        "los": 0.05,
        "reflection": 0.40,
        "diffraction": 0.05,
        "scattering": 0.40,
        "penetration": 0.10
      },
    
      "pathloss_level_hint": "high",
    
      "los_region_hint": "LOS regions are strongly reduced because pedestrians may block or weaken the direct path.",
      "nlos_region_hint": "NLOS-like regions may appear behind dense pedestrian groups and around blocked street segments.",
      "shadowing_region_hint": "Strong local shadowing is expected behind groups of pedestrians and around crowded areas.",
      "blockage_region_hint": "Dense pedestrian groups are the main dynamic blockage sources, while nearby buildings may also create static blockage.",
    
      "reflection_region_hint": "Reflected components from building facades and nearby walls may help maintain coverage when the direct path is blocked.",
      "diffraction_region_hint": "Diffraction around human bodies and building edges is weak at 28 GHz and contributes only slightly.",
      "scattering_region_hint": "Strong scattering may occur from pedestrians, vehicles, rough walls, and street objects.",
    
      "building_density_hint": "high",
      "material_hint": "Human bodies strongly attenuate 28 GHz signals, while nearby concrete and glass facades may provide reflected or scattered components.",
      "effective_scatterer_hint": "Pedestrians, nearby building facades, vehicles, and street objects are likely effective scatterers.",
    
      "spatial_variation_hint": "Spatial variation is strong and dynamic, with localized high-loss regions around pedestrian blockage areas.",
      "map_pattern_hint": "The generated pathloss map should show localized high-pathloss shadow regions behind pedestrian groups, while reflected and scattered paths may partially support coverage around nearby buildings.",
    
      "conditioning_summary": "For dense urban 28 GHz heavy pedestrian blockage radio map generation, the prior should emphasize dynamic blockage, strong local shadowing, increased scattering, and localized high-pathloss regions."
    }
```
* * *

## Usage

When generating a new radio-map-oriented prior, provide:

1. `system_prompt_radiomap_v2.md`
2. `demonstrations_radiomap_v2.md`
3. the new input case

The output should be a valid JSON object following `radiomap_prior_schema_v2.py`.