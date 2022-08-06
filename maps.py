import pandas as pd
from utils import entity_to_entity_data, REGIONS, get_iso_alpha, supplier_number
import plotly.express as px


def create_map(region, ppe_list, year):
    dfs = []
    for r in REGIONS:
        if r != region:
            df = entity_to_entity_data(region, r)
            for ppe in ppe_list:
                dfs.append(df[df.ppe == f"'{ppe}"].copy())
                dfs[-1]["dest_region"] = r

    raw_data = pd.concat(dfs)

    cols = list({k for k in raw_data.dest_region})
    region_data = pd.DataFrame(columns=cols)

    total_ppe = []
    for dest in cols:
        total_ppe.append(sum(raw_data[raw_data.dest_region == dest][year]))
    region_data.loc["total_ppe"] = total_ppe

    for ppe in ppe_list:
        single_ppe = []
        for dest in cols:
            single_ppe.append(raw_data[(raw_data.dest_region == dest) &
                                       (raw_data.ppe == f"'{ppe}")][year].to_numpy(int)[0])
        region_data.loc[ppe] = single_ppe

    cols = ["iso_alpha", "region", "supplier number", "total exported ppe"]
    cols.extend(ppe_list)
    map_data = pd.DataFrame(columns=cols)

    i = 0
    for r in REGIONS:
        if r != region:
            supplier_num = supplier_number(r)["Sum"]
            iso_alphas = get_iso_alpha(r)
            for iso_alpha in iso_alphas:
                item = [iso_alpha, r, supplier_num, region_data[r]["total_ppe"]]
                for ppe in ppe_list:
                    item.append(region_data[r][ppe])
                map_data.loc[i] = item
                i += 1

    map_data["total exported ppe"] = map_data["total exported ppe"].astype(float)
    hover_data = {"iso_alpha": False, "supplier number": True}
    for ppe in ppe_list:
        hover_data[ppe] = True

    fig = px.choropleth(
        map_data,
        locations="iso_alpha",
        color="total exported ppe",  # lifeExp is a column of gapminder
        hover_name="total exported ppe",  # column to add to hover information
        color_continuous_scale=px.colors.sequential.Plasma,
        hover_data=hover_data
    )
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 10})

    return fig


def _tc0():
    fig = create_map("US", ["630790", "392690"], "2017")
    fig.show()


if __name__ == '__main__':
    _tc0()
