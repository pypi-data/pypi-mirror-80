import pytest

from instawow import exceptions as E
from instawow.models import Pkg
from instawow.resolvers import Defn, Strategies


@pytest.fixture(autouse=True)
def mock(mock_all):
    pass


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'strategy', [Strategies.default, Strategies.latest, Strategies.any_flavour]
)
async def test_resolve_curse_simple_pkgs(manager, request, strategy):
    results = await manager.resolve(
        [
            Defn.get('curse', 'tomcats').with_strategy(strategy),
            Defn.get('curse', 'mythic-dungeon-tools').with_strategy(strategy),
            Defn.get('curse', 'classiccastbars').with_strategy(strategy),
            Defn.get('curse', 'elkbuffbars').with_strategy(strategy),
        ]
    )
    separate, retail_only, classic_only, flavour_explosion = results.values()

    assert isinstance(separate, Pkg)
    if manager.config.is_classic:
        if strategy is Strategies.any_flavour:
            assert 'classic' not in separate.version
            assert isinstance(retail_only, Pkg)
        else:
            assert 'classic' in separate.version
            assert (
                isinstance(retail_only, E.PkgFileUnavailable)
                and retail_only.message
                == f"no files compatible with classic using '{strategy.name}' strategy"
            )
        assert isinstance(classic_only, Pkg)
    else:
        assert 'classic' not in separate.version
        assert isinstance(retail_only, Pkg)
        if strategy is Strategies.any_flavour:
            assert isinstance(classic_only, Pkg)
        else:
            assert (
                isinstance(classic_only, E.PkgFileUnavailable)
                and classic_only.message
                == f"no files compatible with retail using '{strategy.name}' strategy"
            )

    versions = {*request.config.cache.get('flavour_explosion', ()), flavour_explosion.version}
    assert len(versions) == 1
    request.config.cache.set('flavour_explosion', tuple(versions))


@pytest.mark.asyncio
async def test_resolve_curse_latest_pkg(manager):
    (latest_pkg,) = (
        await manager.resolve([Defn.get('curse', 'tomcats').with_strategy(Strategies.latest)])
    ).values()
    assert latest_pkg.options.strategy == 'latest'


@pytest.mark.asyncio
async def test_resolve_curse_versioned_pkg(manager):
    (versioned_pkg,) = (
        await manager.resolve([Defn.get('curse', 'molinari').with_version('70300.51-Release')])
    ).values()
    assert (
        versioned_pkg.options.strategy == 'version' and versioned_pkg.version == '70300.51-Release'
    )


@pytest.mark.asyncio
async def test_resolve_curse_deps(manager):
    if manager.config.is_classic:
        pytest.skip('no classic equivalent')

    defns = [Defn.get('curse', 'mechagon-rare-share').with_strategy(Strategies.default)]
    with_deps = await manager.resolve(defns, with_deps=True)
    assert ['mechagon-rare-share', 'rare-share'] == [d.slug for d in with_deps.values()]


@pytest.mark.asyncio
async def test_resolve_wowi_pkgs(manager):
    results = await manager.resolve(
        [
            Defn.get('wowi', '13188-molinari'),
            Defn.get('wowi', '13188').with_strategy(Strategies.latest),
        ]
    )
    either, invalid = results.values()

    assert isinstance(either, Pkg)
    assert (
        isinstance(invalid, E.PkgStrategyUnsupported)
        and invalid.message == "'latest' strategy is not valid for source"
    )


@pytest.mark.asyncio
async def test_resolve_tukui_pkgs(manager):
    results = await manager.resolve(
        [
            Defn.get('tukui', '1'),
            Defn.get('tukui', '-1'),
            Defn.get('tukui', 'tukui'),
            Defn.get('tukui', '1').with_strategy(Strategies.latest),
        ]
    )
    either, retail_id, retail_slug, invalid = results.values()

    assert isinstance(either, Pkg)
    if manager.config.is_classic:
        assert either.name == 'Tukui'
        assert isinstance(retail_id, E.PkgNonexistent)
        assert isinstance(retail_slug, E.PkgNonexistent)
    else:
        assert either.name == 'MerathilisUI'
        assert isinstance(retail_id, Pkg) and retail_id.name == 'Tukui'
        assert isinstance(retail_slug, Pkg) and retail_slug.name == 'Tukui'
    assert (
        isinstance(invalid, E.PkgStrategyUnsupported)
        and invalid.message == "'latest' strategy is not valid for source"
    )


@pytest.mark.asyncio
async def test_resolve_github_pkgs(manager):
    results = await manager.resolve(
        [
            Defn.get('github', 'AdiAddons/AdiButtonAuras'),
            Defn.get('github', 'AdiAddons/AdiButtonAuras').with_version('2.1.0'),
            Defn.get('github', 'AdiAddons/AdiButtonAuras').with_version('2.0.19'),
            Defn.get('github', 'WeakAuras/WeakAuras2'),
            Defn.get('github', 'p3lim-wow/Molinari'),
            Defn.get('github', 'layday/foo-bar'),
        ]
    )
    (
        lib_and_nolib,
        older_version,
        assetless,
        retail_and_classic,
        releaseless,
        missing,
    ) = results.values()
    assert 'nolib' not in lib_and_nolib.download_url
    assert older_version.options.strategy == 'version' and older_version.version == '2.1.0'
    assert isinstance(assetless, E.PkgFileUnavailable)
    assert (
        isinstance(releaseless, E.PkgFileUnavailable)
        and releaseless.message == 'release not found'
    )
    assert ('classic' in retail_and_classic.download_url) is manager.config.is_classic
    assert isinstance(missing, E.PkgNonexistent)
