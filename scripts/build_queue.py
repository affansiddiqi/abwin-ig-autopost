#!/usr/bin/env python3
"""Builds queue.json: an ordered, round-robin list of {image, caption} posts.

Captions reuse only the benefit/ingredient language already verified against
each product's real supplement facts label during the ABWIN Shopify redesign
project (no new or invented health claims).
"""
import json
import os

IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "images")

PRODUCTS = {
    "alphavin360": {
        "handle": "alphavin360",
        "images": [
            "alphavin360-b-raw-gym-v2.jpg",
            "alphavin360-controlled-power-v1.jpg",
            "alphavin360-j-lineup-6in1-v3.jpg",
            "b01-alpha-l-desk.jpg",
            "b02-alpha-n-constellation.jpg",
            "b03-alpha-c-botanical.jpg",
            "b04-alpha-m-dawn.jpg",
        ],
        "hooks": [
            "Gym sessions feel flat lately? Low drive isn't something you have to just accept.",
            "27 actives. 5 individually dosed on the label. Zero guesswork.",
            "Every ingredient named — even inside the support blends. That's the whole point.",
            "Long desk days shouldn't be the reason your energy disappears by 6pm.",
            "Ancient herbal actives, dosed the modern way — nothing hidden behind 'proprietary blend.'",
            "Tribulus. Ashwagandha. Mucuna. Real actives, real doses, real label.",
            "Mornings should feel like you've got something in the tank. That's what this is built for.",
        ],
        "benefits": "Supports men's hormonal balance, helps maintain healthy testosterone levels, and supports muscle mass & athletic performance.",
        "hashtags": "#AlphaVin360 #MensHealthPK #TestosteroneSupport #MensVitality #ABWINLabs #PakistanFitness #NoMoreLowEnergy",
    },
    "femyvin360": {
        "handle": "femyvin360",
        "images": [
            "femyvin360-g-headline-cycle-v3.jpg",
            "femyvin360-k-capsule-hero-v2.jpg",
            "femyvin360-morning-steady-v1.jpg",
            "b08-femy-l-bedroom.jpg",
            "b09-femy-c-roots.jpg",
            "b10-femy-a-kitchen.jpg",
            "b11-femy-n-inositol.jpg",
        ],
        "hooks": [
            "Irregular cycles, mood swings, that 'my hormones are off' feeling — you're not imagining it.",
            "32 actives. Every single one individually dosed. No unnamed proprietary blend anywhere.",
            "Some mornings your body needs steadier support than coffee can give it.",
            "Restless nights during hormonal shifts are real — and worth actually addressing.",
            "Rooted in traditional actives like Ashwagandha and Asparagus Racemosus, dosed with real numbers.",
            "Your kitchen routine already has room for one more steady habit.",
            "D-Chiro and Myo-Inositol, dosed on the real label — not buried in a blend.",
        ],
        "benefits": "Supports women's hormonal balance, healthy regular menstrual cycles, and mood balance & stress response.",
        "hashtags": "#Femyvin360 #WomensHealthPK #HormonalBalance #PCOSsupportPK #ABWINLabs #WomensWellness #CycleSupport",
    },
    "gluthavin360": {
        "handle": "gluthavin360",
        "images": [
            "gluthavin360-c-splash-500mg-v2.jpg",
            "gluthavin360-e-skin-layers-v3.jpg",
            "gluthavin360-light-from-within-v1.jpg",
            "b05-gluth-d-callouts.jpg",
            "b06-gluth-m-editorial.jpg",
            "b07-gluth-k-capsule.jpg",
        ],
        "hooks": [
            "500mg of Reduced Glutathione (98%) — the number that's actually on the label.",
            "Dull, tired-looking skin isn't just a 'me' problem. It's a support problem.",
            "Glow that starts from within, not from a filter.",
            "13 actives. Every one individually dosed, nothing hidden.",
            "Uneven tone, visible tiredness — this is what the formula is built to work on.",
            "One capsule, a real ingredient list you can actually read end to end.",
        ],
        "benefits": "Supports skin radiance & glow, an even skin tone, and antioxidant defense against skin-aging stress.",
        "hashtags": "#Gluthavin360 #GlutathionePK #SkinGlowPK #ClearSkinJourney #ABWINLabs #SkinRadiance #EvenSkinTone",
    },
    "ostyall": {
        "handle": "ostyall",
        "images": [
            "ostyall-a-staircase-v2.jpg",
            "ostyall-d-callouts-calcium-v3.jpg",
            "ostyall-movement-uninterrupted-v1.jpg",
            "b12-osty-f-joint.jpg",
            "b13-osty-b-counter.jpg",
            "b14-osty-m-stairs.jpg",
            "b18-osty-k-four.jpg",
        ],
        "hooks": [
            "Stairs shouldn't be the thing you dread most about your day.",
            "18 actives, organized into 6 support pillars — every one individually dosed.",
            "Movement you don't have to think twice about — that's the goal.",
            "Joint stiffness creeping in earlier than it should? Worth addressing head-on.",
            "On the counter, in the routine, every single day — consistency is the whole strategy.",
            "Bone Matrix, Cartilage Generation, Anti-Inflammatory support — all named, all dosed.",
            "Four capsules, six support pillars, zero unnamed blends.",
        ],
        "benefits": "Supports healthy bone mass, joint mobility, and cartilage health.",
        "hashtags": "#OstyALL #JointHealthPK #BoneHealthPK #MobilityMatters #ABWINLabs #JointSupport #ActiveAging",
    },
    "magnyall": {
        "handle": "magnyall",
        "images": [
            "magnyall-n-absorption-v4.jpg",
            "magnyall-o-bedside-v3.jpg",
            "magnyall-quiet-v1.jpg",
            "magnyall-quiet-v2.jpg",
            "b15-magny-g-314am.jpg",
            "b16-magny-h-pedestal.jpg",
            "b17-magny-k-hand.jpg",
        ],
        "hooks": [
            "3:14am and wide awake again? Your magnesium levels might be part of the story.",
            "Chelated Magnesium BisGlycinate — better absorbed, gentler on digestion.",
            "7 actives, every one individually disclosed. No proprietary blend anywhere.",
            "The quiet you're looking for at 11pm doesn't have to stay out of reach.",
            "Bedside table, every night, same routine — that's how support actually works.",
            "Racing thoughts at bedtime aren't just 'a busy mind' — sometimes it's what's missing from your day.",
            "One capsule, real dosing, on a label you can actually read.",
        ],
        "benefits": "Supports better sleep quality, calmness & relaxation, and mental clarity & focus.",
        "hashtags": "#MagnyAll #MagnesiumPK #SleepSupportPK #StressReliefPK #ABWINLabs #BetterSleep #CalmMind",
    },
    "slimyfire-plus": {
        "handle": "slimyfire-plus",
        "images": [
            "slimyfire-plus-5-capsules-in-one-v1.jpg",
            "b19-slimy-g-11pm.jpg",
            "b20-slimy-c-garcinia.jpg",
        ],
        "hooks": [
            "5 core actives, individually dosed, plus one fully named support blend — no mystery ingredients.",
            "11pm cravings hit different when your metabolism is already working against you.",
            "Garcinia Cambogia 10:1, dosed the way the label actually says — not just a marketing word.",
        ],
        "benefits": "Supports a healthy metabolic rate, fat metabolism, and appetite & craving control.",
        "hashtags": "#SlimyfirePlus #WeightManagementPK #MetabolismSupport #CravingControl #ABWINLabs #HealthyWeightPK",
    },
}

CTA = "\n\nDRAP-registered · GMP-certified facility · Every ingredient named.\nShop now — link in bio 🔗"


def build_caption(product_key, idx):
    p = PRODUCTS[product_key]
    hook = p["hooks"][idx % len(p["hooks"])]
    return f"{hook}\n\n{p['benefits']}{CTA}\n\n{p['hashtags']}"


def main():
    # Round-robin interleave across products for feed variety.
    per_product_iters = {k: iter(enumerate(v["images"])) for k, v in PRODUCTS.items()}
    queue = []
    exhausted = set()
    while len(exhausted) < len(PRODUCTS):
        for key in PRODUCTS:
            if key in exhausted:
                continue
            try:
                idx, image = next(per_product_iters[key])
            except StopIteration:
                exhausted.add(key)
                continue
            queue.append(
                {
                    "id": f"{key}-{idx+1:02d}",
                    "product": key,
                    "image": image,
                    "caption": build_caption(key, idx),
                    "posted": False,
                    "posted_at": None,
                }
            )

    out_path = os.path.join(os.path.dirname(__file__), "..", "queue.json")
    with open(out_path, "w") as f:
        json.dump(queue, f, indent=2, ensure_ascii=False)
    print(f"Wrote {len(queue)} items to {out_path}")


if __name__ == "__main__":
    main()
