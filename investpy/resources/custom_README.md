# custom_*.csv overlay registries

Hand-captured rows for instruments absent from Investing.com's bulk registry
exports. Loaded via investpy.utils.resources.load_registry, which overlays each
custom_<class>.csv onto the upstream <class>.csv.

curr_ids captured 2026-07-10 from investpy.search_quotes(text=...).id_.
If a direct lookup starts raising ERR#0054/0045 (id retired), re-capture the id
via search_quotes and update the row here.
