import glob
import os

from numpy import nan
import pandas as pd

from tools.retools import *


def set_nested_dictionary(d_, root, one, two=None):
    m_two = set(two) if two else set()

    try:
        d_[root][one].add(two)
    except KeyError:
        try:
            d_[root].update({one: m_two})
        except KeyError:
            d_[root] = {one: m_two}
        except TypeError:
            d_[root].update({one: set()})


def deep(*args, d=None):
    root = args[0]
    if not d:
        d = {}
    if isinstance(args, tuple):
        args = [data for data in args]
    for arg in args[1:]:
        d[root] = {arg, deep(args[1:], d)}
    return d


def is_dir(lazy_path):
    path_list = [
        globed
        for globed in glob.glob(r"{}".format(lazy_path + "/*"))
        if os.path.isdir(globed)
    ]
    return path_list


def tools_generate_used_techniques_from_raw(path):
    technique_lims = {}
    techniques = {"FTIR", "SEM", "EDS", "OptDigMicr", "mFTIR", "TG"}
    bad_optical = {r"(OptDig)(.+)?(?=_)", r"(Optic)(.+)?(?=_)"}

    m_search_strings = re_search_strings()

    for current_path, dir_in_cur_path, files_in_cur_path, in os.walk(path):
        for directory in dir_in_cur_path:
            used_techniques = [data for data in re_extract(directory, techniques)]
            bad_tech = [data for data in re_extract(directory, bad_optical)]
            for bad in bad_tech:
                # TODO: Refactor this side effect
                temp = directory.replace(
                    re.search(bad, directory).group(0), "OptDigMicr"
                )
                new_directory = os.path.join(path, temp)
                old_directory = os.path.join(path, directory)
                used_techniques = ["OptDigMicr"]
                try:
                    os.rename(old_directory, new_directory)
                except FileNotFoundError:
                    pass
            files = glob.glob(os.path.join(current_path, directory + "\\*"))
            for file in files:
                m_lims = re_extract_try(
                    file.split("\\")[-1],
                    m_search_strings["seach_string_LIMS_in_files_Future"],
                    0,
                )
                if m_lims:
                    try:
                        set_nested_dictionary(
                            technique_lims, used_techniques[0], m_lims, "x"
                        )
                    except:
                        pass

    return technique_lims


def lazy_lims_new(root):
    from collections import defaultdict

    path_list = is_dir(root)
    lims_dict = defaultdict()
    techniques = {"FTIR", "SEM", "EDS", "OptDigMicr", "mFTIR", "TG"}
    for path in path_list:
        for current_path, dir_in_cur_path, files_in_cur_path, in os.walk(path):
            for file in files_in_cur_path:
                try:
                    date, lims, name = os.path.splitext(file)[0].split("_")
                    tech = [d for d in re_extract(current_path, techniques)][0]
                    old_name = lims_dict.get(lims, {}).get("Name")
                    if lims_dict.get(lims):
                        lims_dict[lims]["Name"] = (
                            old_name
                            if (old_name and len(old_name) < len(name))
                            else name
                        )
                        lims_dict[lims][tech] = "x"
                    else:
                        lims_dict[lims] = {"Name": name, tech: "x"}
                except ValueError as e:
                    print(e, file)
                    continue

    t = pd.DataFrame.from_dict(lims_dict).transpose().reset_index()
    t["Lims_Name"] = t[["Name", "index"]].apply(lambda x: " ".join(x), axis=1)
    t = t.drop(columns=["Name"])
    t.set_index("index", inplace=True)
    t.sort_index(inplace=True)
    ordered_tech = ["Lims_Name", "OptDigMicr", "FTIR", "SEM", "EDS"]
    for tech in ordered_tech:
        if tech not in t:
            t[tech] = ""
    t = t[ordered_tech]
    t.index.name = "LIMS"
    t.to_csv(root + "\\lims.csv", sep=";")


def lazy_lims(lazy_path):
    m_search_strings = re_search_strings()
    path_list = is_dir(lazy_path)
    lims_sample_container = {}
    lims_index = []
    tech = tools_generate_used_techniques_from_raw(lazy_path)

    for path in path_list:
        for current_path, dir_in_cur_path, files_in_cur_path, in os.walk(path):
            for file in files_in_cur_path:
                if not re_extract_try(
                    file, m_search_strings["search_string_spectrum_csv"]
                ):
                    m_free_text = re_extract_try(
                        file,
                        m_search_strings[
                            "search_string_match_all_after_last_underscore"
                        ],
                        0,
                    )
                    if m_free_text:
                        m_free_text = m_free_text.split(".")[0]
                    m_lims = re_extract_try(
                        file, m_search_strings["seach_string_LIMS_in_files_Future"], 0
                    )
                    if m_lims:
                        lims_index.append(m_lims)
                    if m_lims and m_free_text:
                        if lims_sample_container.get(m_lims):
                            lims_sample_container[m_lims].add(m_free_text)
                        else:
                            lims_sample_container[m_lims] = {m_free_text}

    # Logically the shortest name should be the correct sample name
    # This fails when there are multiple samples attached to a given lims
    for k, v in lims_sample_container.items():
        lims_sample_container[k] = min(filter(None, v), key=len)
    lims_index_set = set(lims_index)
    lims_index = list(lims_index_set)
    lims_index.sort()
    dls = ["{0} {1}".format(v, k) for k, v in lims_sample_container.items()]

    # Ensures we're sorting by LIMS #
    dls = sorted(dls, key=lambda x: x.split(" ")[-1])
    lazy_data = pd.DataFrame(index=lims_index, data=dls, columns=["LIMS"])
    ordered_tech = ["OptDigMicr", "FTIR", "SEM", "EDS"]

    for order in ordered_tech:
        lazy_data[order] = nan
        for k, v in tech.items():
            if k == order:
                for kk, vv in v.items():
                    lazy_data.loc[kk, k] = next(iter(vv))

    lazy_data.fillna("na", inplace=True)
    lazy_data.to_csv(lazy_path + "\\lims and sample.csv", sep=";")

    lims_frame = pd.DataFrame(data=lims_index)
    lims_frame.to_csv(lazy_path + "\\lims.csv", sep=";")


def reshape_spectral_csv(lazy_path):
    elemental_dictionary = {
        "Ni": "Nickel (%)",
        "Si": "Silicon (%)",
        "Mg": "Magnesium (%)",
        "Al": "Aluminum (%)",
        "K": "Potassium (%)",
        "Ca": "Calcium (%)",
        "Cu": "Copper (%)",
        "Zr": "Zirconium (%)",
        "Mo": "Molybdenum (%)",
        "Ag": "Silver (%)",
        "Au": "Gold (%)",
        "Sn": "Tin (%)",
        "W": "Tungsten (%)",
        "Cr": "Chromium (%)",
        "Fe": "Iron (%)",
        "S": "Sulfur (%)",
        "Cl": "Chlorine (%)",
        "Zn": "Zinc (%)",
        "P": "Phosphor (%)",
        "Pb": "Lead (%)",
        "Ne": "Neon (%)",
        "Ti": "Titanium(%)",
        "Mn": "Manganese (%)",
    }

    path_list = is_dir(lazy_path)
    for p in path_list:
        if re.search("SEM", p) or re.search("EDS", p):
            try:
                spectra = glob.glob(p + "\\*.csv")
                eds_frame = pd.read_csv(spectra[0], skiprows=2, index_col="Name")
                eds_frame.rename(columns=elemental_dictionary, inplace=True)
                hold = []
                for i in eds_frame.values:
                    temp_hold = []
                    for index, value, in enumerate(i):
                        value = str(value)
                        if value not in " ":
                            temp_hold.append(
                                "{} {}".format(value, eds_frame.columns[index])
                            )
                    hold.append(temp_hold)
                e = eds_frame.reset_index()
                cleaned = pd.DataFrame(
                    data=hold,
                    index=e["Name"].apply(
                        lambda x: " ".join("_".join(x.split("_")[::-1]).split("_")[:-1])
                    ),
                )
                with open(lazy_path + "\\cleaned_spectrum.csv", "w") as lzy:
                    cleaned.to_csv(
                        lzy, sep=";", header=True, index=True, line_terminator="\n"
                    )
            except Exception as e:
                print(e)
                pass
