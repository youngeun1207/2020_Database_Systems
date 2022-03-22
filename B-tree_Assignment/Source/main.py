import sys
from math import floor
import csv

args = sys.argv
index = 0


class BpNode(object):
    def __init__(self, max):
        self.max = max
        self.key = []
        self.parent: BpNode = None
        self.children: BpNode[max] = None

    def isLeaf(self):
        return False

    def isFull(self):
        return len(self.key) >= self.max

    def isUnderflow(self):
        return len(self.key) < floor((self.max) / 2)

    def cannotBorrow(self):
        return len(self.key) - 1 < floor((self.max) / 2)

    def split(self):
        # Index 나누기
        center = self.max // 2
        center_key = self.key[center]
        rightNode = BpNode(self.max)
        rightNode.key = self.key[center + 1:]
        self.key = self.key[:center]
        i = center + 1
        while len(self.children) > i:
            self.children[i].parent = rightNode
            i += 1
        rightNode.children = self.children[center + 1:]
        self.children = self.children[:center + 1]

        # Root node
        if self.parent is None:
            parent = BpNode(self.max)
            parent.key.append(center_key)
            self.parent = parent
            rightNode.parent = parent
            parent.children = [self, rightNode]
        # 이미 부모 노드가 있는 경우
        else:
            rightNode.parent = self.parent
            i = 0
            while i < len(self.parent.key):
                if self.parent.key[i] > center_key:
                    break
                i = i + 1
            self.parent.key.insert(i, center_key)
            if len(self.parent.children) == i:
                self.parent.children[i - 1] = self
                self.parent.children.append(rightNode)
            else:
                self.parent.children[i] = self
                self.parent.children.insert(i + 1, rightNode)
            # 부모 노드가 꽉 참
            if self.parent.isFull():
                self = self.parent.split()

        while not self.parent is None:
            self = self.parent
        return self

    def borrowLeft(self, sibling, index):  # Left 형제의 부모 인덱스 넣기 (my index - 1)
        parentKey = self.parent.key[index]
        siblingKey = sibling.key.pop(-1)
        nephew = sibling.children.pop(-1)

        nephew.parent = self
        self.parent.key[index] = siblingKey
        self.key.insert(0, parentKey)
        self.children.insert(0, nephew)

    def borrowRight(self, sibling, index):  # 나의 부모 인덱스 넣기
        # rotate key
        parentKey = self.parent.key[index]
        siblingKey = sibling.key.pop(0)
        nephew = sibling.children.pop(0)

        nephew.parent = self
        self.parent.key[index] = siblingKey
        self.key.append(parentKey)
        self.children.append(nephew)


class BpLeaf(BpNode):
    def __init__(self, max):
        super().__init__(max)
        self.right: BpLeaf = None
        self.value = []

    def isLeaf(self):
        return True

    def split(self):
        # Leaf 나누기 (중간값을 기준으로)
        center = self.max // 2
        center_key = self.key[center]
        # 새 노드 만들어주기
        rightNode = BpLeaf(self.max)
        # 복사
        rightNode.key = self.key[center:]
        self.key = self.key[:center]
        rightNode.value = self.value[center:]
        self.value = self.value[:center]
        rightNode.right = self.right
        self.right = rightNode

        # 부모 노드가 없는 경우(Leaf가 Root)
        if self.parent is None:
            parent = BpNode(self.max)
            parent.key.append(center_key)
            self.parent = parent
            rightNode.parent = parent
            parent.children = [self, rightNode]

        # 이미 부모 노드가 있는 경우
        else:
            rightNode.parent = self.parent
            i = 0
            while i < len(self.parent.key):
                if self.parent.key[i] > center_key:
                    break
                i = i + 1
            self.parent.key.insert(i, center_key)
            if len(self.parent.children) == i:
                self.parent.children[i - 1] = self
                self.parent.children.append(rightNode)
            else:
                self.parent.children[i] = self
                self.parent.children.insert(i + 1, rightNode)

            # 부모 노드가 꽉 참
            if self.parent.isFull():
                self = self.parent.split()
        while self.parent is not None:
            self = self.parent
        return self

    def newItem(self, input_key, input_value):
        # empty node
        if not len(self.key):
            self.key.append(input_key)
            self.value.append(input_value)
            return self
        # not empty -> 위치 찾기
        i = 0
        while i < len(self.key):
            if self.key[i] > input_key:
                break
            i += 1
        # 찾은 index에 넣기
        self.key.insert(i, input_key)
        self.value.insert(i, input_value)
        return self

    def borrowLeft(self, sibling, index):  # Left 형제의 부모 인덱스 넣기 (my index - 1)
        siblingKey = sibling.key.pop(-1)
        siblingValue = sibling.value.pop(-1)

        self.key.insert(0, siblingKey)
        self.value.insert(0, siblingValue)

        self.parent.key[index] = siblingKey

    def borrowRight(self, sibling, index):  # 나의 부모 인덱스 넣기
        siblingKey = sibling.key.pop(0)
        siblingValue = sibling.value.pop(0)

        self.key.append(siblingKey)
        self.value.append(siblingValue)

        self.parent.key[index] = sibling.key[0]


class BpTree(object):
    def __init__(self, max):
        self.root: BpNode = BpLeaf(max)
        self.max: int = max
        self.leaves: BpLeaf[max] = []

    def createTree(self, parent, lines):
        global index
        if index >= len(lines):
            return self
        leaf = lines[index].rstrip('\n')
        index += 1
        if leaf == "LR":
            node = BpLeaf(self.max)
            self.root = node
            return self
        if leaf == "L":
            node = BpLeaf(self.max)
            if (parent is None):
                self.root = node
            lines[index] = lines[index].rstrip('\n').split(' ')
            for i in range(len(lines[index])):
                node.key.append(int(lines[index][i]))
            index += 1

            lines[index] = lines[index].rstrip('\n').split(' ')
            for i in range(len(lines[index])):
                node.value.append(int(lines[index][i]))
            index += 1
            node.parent = parent
            self.leaves.append(node)
            return node

        node = BpNode(self.max)

        if parent is None:
            self.root = node

        lines[index] = lines[index].rstrip('\n').split(' ')
        for i in range(len(lines[index])):
            node.key.append(int(lines[index][i]))
        index += 1
        node.parent = parent
        node.children = []
        i = 0
        while len(node.key) + 1 > i:
            add = self.createTree(node, lines)
            if not node.isLeaf():
                node.children.append(add)
            i += 1
        return node

    def connectLeaf(self):
        i = 0
        while i < len(self.leaves) - 1:
            self.leaves[i].right = self.leaves[i + 1]
            i += 1
        self.leaves = []

    def saveTree(self, node, f):
        if node.isLeaf() and node.parent is None and len(node.key) == 0:
            f.write('LR\n')
            return
        if node.isLeaf():
            f.write('L\n')
            f.write(' '.join(map(str, node.key)) + '\n')
            f.write(' '.join(map(str, node.value)) + '\n')
            return
        f.write('I\n')
        f.write(' '.join(map(str, node.key)) + '\n')
        i = 0
        while len(node.key) + 1 > i:
            self.saveTree(node.children[i], f)
            i += 1

    def indexSearch(self, key):
        node = self.root
        # 리프가 아닐 때 까지 index 따라 내려가기
        i = 0
        while True:
            if i == 0:
                print(",".join(map(str, node.key)))
            if node.isLeaf():
                return node
            elif node.key[i] > key:
                node = node.children[i]
                i = 0
                continue
            elif i + 1 >= len(node.key):
                node = node.children[i + 1]
                i = 0
                continue
            i += 1
        return node

    def singleSearch(self, key):
        node = self.indexSearch(key)
        # 리프 노드에서 key 찾기
        for i in range(len(node.key)):
            # 찾는 key가 있다
            if node.key[i] == key:
                return node.value[i]
            # 찾는 key가 없다
        return None

    def rangeSearch(self, start_key, end_key):
        # node = self.indexSearch(start_key)
        node = self.root
        # 리프가 아닐 때 까지 index 따라 내려가기
        i = 0
        while 1:
            if node.isLeaf():
                break
                # return node
            elif node.key[i] > start_key:
                node = node.children[i]
                i = 0
                continue
            elif i + 1 >= len(node.key):
                node = node.children[i + 1]
                i = 0
                continue
            i += 1
        j = 0
        while True:
            if node is None:
                break
            if j >= len(node.key):
                node = node.right
                j = 0
                continue
            if node.key[j] < start_key:
                j += 1
                continue
            elif node.key[j] > end_key:
                break
            print('<' + str(node.key[j]) + '>' + '<' + str(node.value[j]) + '>')
            j += 1

    def searchPlace(self, key):
        node = self.root
        # 리프가 아닐 때 까지 index 따라 내려가기
        i = 0
        while True:
            if node.isLeaf():
                break
            elif node.key[i] > key:
                node = node.children[i]
                i = 0
                continue
            elif i + 1 >= len(node.key):
                node = node.children[i + 1]
                i = 0
                continue
            i += 1
        for i in range(len(node.key)):
            # 찾는 key가 있다
            if node.key[i] == key:
                return node, node.value[i]
            # 찾는 key가 없다
        return node, False

    def insertNode(self, input):
        input_key = input[0]
        input_value = input[1]
        node, exist = self.searchPlace(input_key)
        if exist:
            print('Key ' + str(input_key) + ' is already exists')
            return self
        # 리프에 공간이 있다.
        if len(node.key) + 1 < node.max:
            node.newItem(input_key, input_value)
        # split 해야함!
        else:
            node.newItem(input_key, input_value)
            node = node.split()
            self.root = node
        return self

    def deleteNode(self, input):
        node, exist = self.searchPlace(input)
        if not exist:
            print("NOT FOUND")
            return self.root
        index = node.key.index(input)
        node.value.pop(index)
        node.key.pop(index)

        while node.isUnderflow() and not node.parent is None:
            i = 0
            while i < len(node.parent.key) and node.parent.key[i] <= input:
                i += 1
            parent = i
            left = self.leftSibling(node, parent)
            right = self.rightSibling(node, parent)
            # borrow
            if right and not right.cannotBorrow():
                node.borrowRight(right, i)
            elif left and not left.cannotBorrow():
                node.borrowLeft(left, i - 1)
            # merge
            elif left and left.cannotBorrow():
                self.merge(left, node, left.key[0])
            elif right and right.cannotBorrow():
                self.merge(node, right, input)

            node = node.parent
        # root is empty
        if len(self.root.key) == 0:
            self.root = self.root.children[0]
            self.root.parent = None

    def leftSibling(self, node, index):
        if node.parent is None or index <= 0:
            return None
        return node.parent.children[index - 1]

    def rightSibling(self, node, index):
        if node.parent is None or index >= len(node.parent.children) - 1:
            return None
        return node.parent.children[index + 1]

    def merge(self, leftNode, rightNode, key):
        parentNode = leftNode.parent
        i = 0
        while i < len(parentNode.key) and parentNode.key[i] <= key:
            i += 1
        index = i
        parent_key = parentNode.key.pop(index)

        if leftNode.isLeaf() and rightNode.isLeaf():
            parentNode.children.pop(index)
            parentNode.children[index] = leftNode
            leftNode.right = rightNode.right
            leftNode.key = leftNode.key + rightNode.key
            leftNode.value = leftNode.value + rightNode.value
        else:
            parentNode.children.pop(index)
            parentNode.children[index] = leftNode
            leftNode.key.append(parent_key)
            for child in rightNode.children:
                child.parent = leftNode

            leftNode.key = leftNode.key + rightNode.key
            leftNode.children = leftNode.children + rightNode.children


def main():
    global index
    ToDo = sys.argv[1]

    rangeSearch = 0
    if ToDo == 'r':
        rangeSearch += 1

    if ToDo == 'c':
        # Create init B+ Tree
        myTree = BpTree(max=int(sys.argv[3]))
        # Save index file
        f = open(sys.argv[2], 'w')
        f.write(str(myTree.max) + '\n')
        myTree.saveTree(myTree.root, f)
        f.close()
        exit()

    else:
        # Load Index File
        f = open(sys.argv[3 + rangeSearch], 'r')
        lines = f.readlines()
        index = 0
        myTree = BpTree(max=int(lines[index]))
        index += 1
        myTree.createTree(None, lines)
        myTree.connectLeaf()
        f.close()

    if ToDo == 'i':
        f = open(sys.argv[2], 'r', encoding='utf-8')
        csv_data = csv.reader(f)
        for line in csv_data:
            line = list(map(int, line))
            myTree = myTree.insertNode(line)
        f.close()

    elif ToDo == 'd':
        f = open(sys.argv[2], 'r', encoding='utf-8')
        csv_data = csv.reader(f)
        for line in csv_data:
            myTree.deleteNode(int(line[0]))
        f.close()

    elif ToDo == 's':
        value = myTree.singleSearch(int(sys.argv[2]))
        if value is not None:
            print("<" + str(value) + ">")
        else:
            print("NOT FOUND")

    elif ToDo == 'r':
        start_key = int(sys.argv[2])
        end_key = int(sys.argv[3])
        myTree.rangeSearch(start_key, end_key)

    # Save index file
    if ToDo == 'd' or ToDo == 'i' or ToDo == 'c':
        f = open(sys.argv[3], 'w')
        f.write(str(myTree.max) + '\n')
        myTree.saveTree(myTree.root, f)
        f.close()


if __name__ == '__main__':
    main()
