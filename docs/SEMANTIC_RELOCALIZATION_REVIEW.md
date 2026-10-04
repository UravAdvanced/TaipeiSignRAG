# SignNav, TS-1M and proposed semantic relocalisation

Verified 2026-10-04 from primary papers and ARCore/Unity documentation. This is research and architecture discussion, not an implemented or measured drift-correction system.

## Papers actually found

- SignNav: Leveraging Signage for Semantic Visual Navigation in Large-Scale Indoor Environments, arXiv:2603.16166 (March 2026). Proposes START and 20 LSI environments. Its dataset design deliberately uses directional arrows without textual information, separating spatial reasoning from OCR/text matching. It is related sign-guided navigation work, not a demonstration of Taipei sign RAG correcting ARCore.
  https://arxiv.org/html/2603.16166v1
- TS-1M is introduced in Traffic Sign Recognition in Autonomous Driving: Dataset, Benchmark, and Field Experiment, arXiv:2603.23034 (March 2026). It comprises over one million traffic-sign images in 454 standardised categories, benchmarks recognition and includes a driving experiment integrating semantics and spatial localisation. The exact supplied title “Mitigating Visual SLAM Odometry Drift using Semantic Landmark Relocalization” was not verified. Do not cite it as TS-1M's title or as an established ARCore loop-closure result.
  https://arxiv.org/html/2603.23034v1
- TextSLAM: Visual SLAM with Semantic Planar Text Features, TPAMI 2023, arXiv:2305.10029. This is more directly relevant: it jointly uses text geometry and semantics, reconstructs a semantic 3D text map, and reports SLAM results. Open code and data are linked by the authors. Text-assisted SLAM itself is already prior art.
  https://arxiv.org/abs/2305.10029
  https://github.com/SJTU-ViSYS/TextSLAM

## Required architecture corrections

1. An ARCore camera pose attached to an image is the observer's pose, not the sign's 3D pose. Register the actual sign/nearby anchor with a shared map using depth, triangulation, suitable geometric correspondences, or another independently established mapping method. Public historical TibaMe frames have no ARCore poses to recover just by running an LLM.
2. Raw ARCore XYZ values are session estimates and can change as tracking is refined. Google explicitly recommends anchors or positions relative to nearby anchors for persistence. A drifting walk does not generate independent absolute ground truth merely by saving its own estimates.
3. Matching a sign ID establishes an association, not the camera's 6-DoF pose. If the camera is four metres from the sign, subtracting their positions treats a real separation as drift. Pose estimation needs relative geometry and orientation, or successful resolution of a registered Cloud Anchor. Sign arrows encode destination directions, not camera orientation measurements.
4. The public ARCore API does not offer the proposed general setter to inject an externally chosen camera pose into its internal SLAM graph. In Unity, an app can adjust its map-to-session alignment / XR Origin after obtaining a validated pose. That changes application alignment, not ARCore's internal SLAM optimisation. Unity's MoveCameraToWorldLocation explicitly moves XR Origin to position the camera in application world coordinates.
5. Spatial filtering requires a shared, already aligned coordinate frame. A hard 15m cutoff can exclude the correct landmark when drift exceeds that radius; retain wider/global recovery and uncertainty-aware candidates. Floor and connectivity constraints help disambiguate, but do not eliminate false matches.
6. ARCore tracking does not itself implement pedestrian obstacle avoidance, step counting or voice guidance. Those are app/subsystem responsibilities.

## Best fit for the existing Cloud Anchor plan

Capture -> recognise candidate sign using the reviewed image/text database -> retrieve registered candidate Cloud Anchor IDs -> resolve against the mapped surrounding features -> obtain consistent map/session alignment -> provide grounded route/sign explanations through RAG and an LLM.

Here RAG helps select the place/anchor and explain sign semantics. Cloud Anchor resolution supplies spatial correspondence. It still requires connectivity, a previously hosted feature map, sufficient current visual features and a valid anchor; semantic recognition does not bypass those requirements.

If implementing custom sign-based geometric relocalisation later, estimate the camera pose in the map frame using a calibrated camera and mapped geometric correspondences; validate it before updating application alignment. With T_map_camera as the geometric estimate and T_session_camera as the current ARCore camera pose, T_map_session = T_map_camera * inverse(T_session_camera). Both rotation and translation matter. Outlier rejection and current tracking quality are necessary; no sign-match confidence alone justifies snapping the user to a landmark coordinate.

## Current deliverable and claims

Proceed with reviewed semantic annotations, evidence-linked image relationships and immediate RAG. Add optional fields for later physical sign/Cloud Anchor associations, without inventing coordinates. Sign-guided selection of Cloud Anchors is a feasible integration hypothesis; improved relocalisation or drift reduction remains unmeasured.

Suggested current title: “TaipeiSignRAG: A Linked Multilingual Signboard Dataset for Grounded Indoor Navigation Assistance.” A later paper can claim relocalisation improvements only after implementation and measured evidence. Neither a proposed architecture nor three named contributions guarantees paper acceptance.

## Primary platform references

- ARCore anchors and world-space updates: https://developers.google.com/ar/develop/anchors
- Pose persistence/frame warnings: https://developers.google.com/ar/reference/java/com/google/ar/core/Pose
- Hosting/resolving Cloud Anchors and connectivity: https://developers.google.com/ar/develop/cloud-anchors
- ARCore public Session API: https://developers.google.com/ar/reference/java/com/google/ar/core/Session
- Camera pose getter: https://developers.google.com/ar/reference/java/com/google/ar/core/Camera
- Unity XROrigin application alignment: https://docs.unity3d.com/Packages/com.unity.xr.core-utils@2.2/api/Unity.XR.CoreUtils.XROrigin.html

Fetched source captures: `research/indoor_6h/semantic_relocalization_*.json`. Search engines returned limited/noisy results for the supplied TS-1M title; scholarly index results were followed to the actual primary paper.
