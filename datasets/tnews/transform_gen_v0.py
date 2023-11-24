import random


def transform(data, num_sample: int, r: random.Random, dataset_name: str):
    tnews_labels = [
        "农业新闻",  # news_agriculture
        "旅游新闻",  # news_travel
        "游戏新闻",  # news_game
        "科技类别公司新闻",  # news_tech
        "体育类别新闻",  # news_sports
        "初升高教育新闻",  # news_edu
        "娱乐圈新闻",  # news_entertainment
        "投资资讯",  # news_finance
        "军事类别常识",  # news_military
        "车辆新闻",  # news_car
        "楼市新闻",  # news_house
        "环球不含中国类别新闻",  # news_world
        "书籍文化历史类别新闻",  # news_culture
        "故事类别新闻",  # news_story
        "股票市场类别新闻",  # news_stock
    ]
    _tnews_options_list_str = "\n".join(
        f'{chr(ord("A") + i)}. {tnews_labels[i]}' for i in range(len(tnews_labels))
    )
    _tnews_options_range_str = "，".join(
        f'“{chr(ord("A") + i)}”' for i in range(len(tnews_labels))
    )
    text = f"{data['question']}\n请判断上述内容属于什么新闻？\n{_tnews_options_list_str}\n请从{_tnews_options_range_str}中进行选择。\n答："
    index_of_correct_answer = list(data["target_scores"].values()).index(1)
    answers = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
    ]
    correct_answer = answers[index_of_correct_answer]

    return {"input": text, "output": correct_answer, "processed_output": correct_answer}
