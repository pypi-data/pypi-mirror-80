"""
Name : Classifier.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-08 10:52
Desc:
"""

import os
import random
import shutil

import torch
from torchvision import transforms, datasets
from ..libs.resnet.network import Network

__all__ = ['train_test_split', 'Classifier']


def train_test_split(src_dir, to_dir, rate=0.3):
    path_dir = os.listdir(src_dir)  # 取图片的原始路径
    file_number = len(path_dir)
    pick_number = int(file_number * rate)  # 按照rate比例从文件夹中取一定数量图片
    sample = random.sample(path_dir, pick_number)  # 随机选取picknumber数量的样本图片
    for name in sample:
        shutil.move(os.path.join(src_dir, name), os.path.join(to_dir, name))
    return


class Classifier(Network):
    def __init__(self, model_name="resnet_checkpoint.pth.tar", ctx_id=-1):
        """
        图像分类
        :param model_name: 模型路径
        :param ctx_id: 指定GPU，-1表示CPU
        """
        super(Classifier, self).__init__(model_name, ctx_id)
        self.model = self.load_model()

    @staticmethod
    def transform_data():
        """
        数据增强函数，可改写
        :return:
        """
        data_transforms = {
            'train': transforms.Compose([
                transforms.Resize((224, 224)),
                # transforms.RandomCrop(224),
                transforms.RandomVerticalFlip(),
                transforms.RandomHorizontalFlip(),
                transforms.RandomRotation(45),
                transforms.ToTensor()
            ]),
            'val': transforms.Compose([
                transforms.Resize((224, 224)),
                # transforms.CenterCrop(224),
                transforms.ToTensor()
            ])
        }

        return data_transforms

    def load_model(self):
        """
        加载模型，可改写
        :return:
        """
        model = torch.load(self.model_name, map_location=None if torch.cuda.is_available() else 'cpu')
        if torch.cuda.is_available():
            model = model.to(self.device)

        return model

    def predict(self, image):
        """
        图像预测
        :param image: 输入图像（numpy data）
        :return: 分类类别
        """
        from PIL import Image
        temp = Image.fromarray(image).convert("RGB")
        transform = self.transform_data()["val"]
        image_tensor = transform(temp).float()
        image_tensor = image_tensor.unsqueeze_(0)

        if torch.cuda.is_available():
            image_tensor = image_tensor.to(self.device)

        output = self.model(image_tensor)
        _, index = torch.max(output.data, 1)

        return int(index)

    def compute_accuracy(self, data_dir, batch_size=32):
        transform = self.transform_data()["val"]
        dataset = datasets.ImageFolder(data_dir, transform)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)

        correct_pred, num_examples = 0, 0
        for i, (features, targets) in enumerate(data_loader):
            features = features.to(self.device)
            targets = targets.to(self.device)

            output = self.model(features)
            _, index = torch.max(output.data, 1)

            num_examples += targets.size(0)
            correct_pred += (index == targets).sum()

        return correct_pred.float() / num_examples * 100
