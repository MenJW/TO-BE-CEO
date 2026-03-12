# License Strategy

## Current State

The repository now uses Apache-2.0.

That choice prioritizes adoption, commercial collaboration, and ecosystem growth over strong copyleft protection.

## Where AGPL Helps

- You want strong reciprocity.
- You want to discourage closed hosted forks.
- You want to force improvements in server deployments back into the commons.

## Where AGPL Hurts

- Some companies will avoid adopting or contributing to it.
- Commercial integrations and enterprise pilots become harder.
- Plugin ecosystems grow more slowly because legal review becomes heavier.

## Better Alternative for Early Ecosystem Growth

Apache-2.0 is usually the best compromise for this kind of orchestration framework.

Why Apache-2.0 instead of MIT:

- It is still permissive.
- It includes an explicit patent grant.
- It is easier to position for enterprise use.
- It works well if you want an open core around workflow primitives while monetizing hosting, templates, data, or premium orchestration services.

## Recommended Decision Rule

Use AGPL-3.0 if your primary objective is protecting the public codebase from closed SaaS forks.

Use Apache-2.0 if your primary objective is adoption, integrations, contributor growth, and enterprise acceptance.

## Suggested Path For This Project

Based on the current idea, the moat is more likely to be:

- workflow design,
- high-quality agent definitions,
- evaluation datasets,
- orchestration UI,
- user experience,
- proprietary hosted operations.

That usually points to Apache-2.0 as the stronger business choice.

## Recommendation

Do not switch licenses casually after public adoption begins.

The repository has already switched from AGPL-3.0 to Apache-2.0.

If future product strategy changes and strong reciprocity becomes more important than adoption, revisit the licensing decision before building major external dependency on the current terms.