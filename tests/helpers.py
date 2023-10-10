from bolt11 import RouteHint


def check_decoded_routes(decoded_route_hints, example_route_hints):
    assert decoded_route_hints
    assert isinstance(decoded_route_hints, list)
    assert len(decoded_route_hints) == len(example_route_hints)
    for i, route_hint in enumerate(decoded_route_hints):
        assert isinstance(route_hint, RouteHint)
        for j, route in enumerate(route_hint.routes):
            ex_route_hint = example_route_hints[i][j]
            assert route.public_key == ex_route_hint["public_key"]
            assert route.short_channel_id == ex_route_hint["short_channel_id"]
            assert route.base_fee == ex_route_hint["base_fee"]
            assert route.ppm_fee == ex_route_hint["ppm_fee"]
            assert route.cltv_expiry_delta == ex_route_hint["cltv_expiry_delta"]
