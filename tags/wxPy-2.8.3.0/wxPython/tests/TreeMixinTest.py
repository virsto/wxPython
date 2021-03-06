import wx, wx.gizmos, wx.lib.customtreectrl, unittest, treemixin


# VirtualTree tests

class TreeCtrl(object):
    def __init__(self, *args, **kwargs):
        self.children = {}
        self.font = {}
        self.colour = {}
        self.bgcolour = {}
        self.image = {}
        self.type = {}
        self.checked = {}
        super(TreeCtrl, self).__init__(*args, **kwargs)

    def OnGetItemFont(self, index):
        return self.font.get(index, wx.NullFont)

    def PrepareItemFont(self, index, font):
        self.font[index] = font

    def OnGetItemTextColour(self, index):
        return self.colour.get(index, wx.NullColour)

    def PrepareItemColour(self, index, colour):
        self.colour[index] = colour

    def OnGetItemBackgroundColour(self, index):
        return self.bgcolour.get(index, wx.NullColour)

    def PrepareItemBackgroundColour(self, index, colour):
        self.bgcolour[index] = colour

    def OnGetItemImage(self, index, which):
        return self.image.get(index, -1)

    def PrepareImage(self, index, imageIndex):
        self.image[index] = imageIndex

    def OnGetItemType(self, index):
        return self.type.get(index, 0)

    def PrepareType(self, index, itemType):
        self.type[index] = itemType

    def OnGetItemChecked(self, index):
        return self.checked.get(index, False)
           
    def PrepareChecked(self, index, checked):
        self.checked[index] = checked


class VirtualTreeCtrlWithTreeIndices(TreeCtrl, treemixin.VirtualTree, 
        wx.lib.customtreectrl.CustomTreeCtrl):

    def __init__(self, *args, **kwargs):
        kwargs['tupleIndex'] = True
        super(VirtualTreeCtrlWithTreeIndices, self).__init__(*args, **kwargs)

    def OnGetItemText(self, indices):
        return 'item %s'%'.'.join([str(index) for index in indices])

    def OnGetChildrenCount(self, index=None):
        index = index or ()
        return self.children.get(index, 0)

    def PrepareChildrenCount(self, index, childrenCount):
        self.children[index] = childrenCount 


class VirtualTreeCtrlWithListIndices(TreeCtrl, treemixin.VirtualTree, 
        wx.lib.customtreectrl.CustomTreeCtrl):

    def __init__(self, *args, **kwargs):
        kwargs['tupleIndex'] = False
        super(VirtualTreeCtrlWithListIndices, self).__init__(*args, **kwargs)

    def OnGetItemText(self, index):
        return 'item %d'%index

    def OnGetChildrenIndices(self, index=None):
        return self.children.get(index, [])

    def PrepareChildrenIndices(self, index, indices):
        self.children[index] = indices 


class VirtualTreeCtrlTestWithTreeIndices_NoRootItems(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(None)
        self.tree = VirtualTreeCtrlWithTreeIndices(self.frame)
        self.tree.RefreshItems()

    def testNoRootItems(self):
        self.assertEqual(0, self.tree.GetCount())

    def testAddTwoRootItems(self):
        self.tree.PrepareChildrenCount((), 2)
        self.tree.RefreshItems()
        self.assertEqual(2, self.tree.GetCount())

    def testAddOneRootItemAndOneChild(self):
        self.tree.PrepareChildrenCount((), 1)
        self.tree.PrepareChildrenCount((0,), 1)
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(2, self.tree.GetCount())

    def testAddOneRootItemAndTwoChildren(self):
        self.tree.PrepareChildrenCount((), 1)
        self.tree.PrepareChildrenCount((0,), 2)
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(3, self.tree.GetCount())


class VirtualTreeCtrlWithListIndicesTest_NoRootItems(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(None)
        self.tree = VirtualTreeCtrlWithListIndices(self.frame)
        self.tree.RefreshItems()

    def testNoRootItems(self):
        self.assertEqual(0, self.tree.GetCount())

    def testAddTwoRootItems(self):
        self.tree.PrepareChildrenIndices(None, [0,1])
        self.tree.RefreshItems()
        self.assertEqual(2, self.tree.GetCount())

    def testAddOneRootItemAndOneChild(self):
        self.tree.PrepareChildrenIndices(None, [0])
        self.tree.PrepareChildrenIndices(0, [1])
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(2, self.tree.GetCount())

    def testAddOneRootItemAndTwoChildren(self):
        self.tree.PrepareChildrenIndices(None, [0])
        self.tree.PrepareChildrenIndices(0, [1,2])
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(3, self.tree.GetCount())


class VirtualTreeCtrlTestWithTreeIndices_OneRoot(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(None)
        self.tree = VirtualTreeCtrlWithTreeIndices(self.frame)
        self.tree.PrepareChildrenCount((), 1)
        self.tree.RefreshItems()

    def testOneRoot(self):
        self.assertEqual(1, self.tree.GetCount())

    def testDeleteRootItem(self):
        self.tree.PrepareChildrenCount((), 0)
        self.tree.RefreshItems()
        self.assertEqual(0, self.tree.GetCount())

    def testAddOneChild(self):
        self.tree.PrepareChildrenCount((0,), 1)
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(2, self.tree.GetCount())

    def testAddTwoChildren(self):
        self.tree.PrepareChildrenCount((0,), 2)
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(3, self.tree.GetCount())

    def testChangeFont(self):
        self.tree.PrepareItemFont((0,), wx.SMALL_FONT)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(wx.SMALL_FONT, self.tree.GetItemFont(item))

    def testChangeColour(self):
        self.tree.PrepareItemColour((0,), wx.RED)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(wx.RED, self.tree.GetItemTextColour(item))

    def testChangeBackgroundColour(self):
        self.tree.PrepareItemBackgroundColour((0,), wx.RED)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(wx.RED, self.tree.GetItemBackgroundColour(item))

    def testChangeImage(self):
        self.tree.PrepareImage((0,), 0)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(0, self.tree.GetItemImage(item))

    def testChangeType(self):
        self.tree.PrepareType((0,), 2)
        self.tree.PrepareChecked((0,), True)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.failUnless(self.tree.IsItemChecked(item))


class VirtualTreeCtrlWithListIndicesTest_OneRoot(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(None)
        self.tree = VirtualTreeCtrlWithListIndices(self.frame)
        self.tree.PrepareChildrenIndices(None, [0])
        self.tree.RefreshItems()

    def testOneRoot(self):
        self.assertEqual(1, self.tree.GetCount())

    def testDeleteRootItem(self):
        self.tree.PrepareChildrenIndices(None, [])
        self.tree.RefreshItems()
        self.assertEqual(0, self.tree.GetCount())

    def testAddOneChild(self):
        self.tree.PrepareChildrenIndices(0, [1])
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(2, self.tree.GetCount())

    def testAddTwoChildren(self):
        self.tree.PrepareChildrenIndices(0, [1,2])
        self.tree.RefreshItems()
        self.tree.ExpandAll()
        self.assertEqual(3, self.tree.GetCount())

    def testChangeFont(self):
        self.tree.PrepareItemFont(0, wx.SMALL_FONT)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(wx.SMALL_FONT, self.tree.GetItemFont(item))

    def testChangeColour(self):
        self.tree.PrepareItemColour(0, wx.RED)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(wx.RED, self.tree.GetItemTextColour(item))

    def testChangeBackgroundColour(self):
        self.tree.PrepareItemBackgroundColour(0, wx.RED)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(wx.RED, self.tree.GetItemBackgroundColour(item))

    def testChangeImage(self):
        self.tree.PrepareImage(0, 0)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.assertEqual(0, self.tree.GetItemImage(item))

    def testChangeType(self):
        self.tree.PrepareType(0, 2)
        self.tree.PrepareChecked(0, True)
        self.tree.RefreshItems()
        item, cookie = self.tree.GetFirstChild(self.tree.GetRootItem())
        self.failUnless(self.tree.IsItemChecked(item))


# TreeAPIHarmonizer tests

class TreeAPIHarmonizerTestCase(unittest.TestCase):
    style = wx.TR_DEFAULT_STYLE

    def setUp(self):
        self.frame = wx.Frame(None)
        class HarmonizedTreeCtrl(treemixin.TreeAPIHarmonizer, self.TreeClass):
            pass
        self.tree = HarmonizedTreeCtrl(self.frame, style=self.style)
        self.populateTree()

    def populateTree(self):
        self.root = self.tree.AddRoot('Root')
        self.item = self.tree.AppendItem(self.root, 'Item')
        self.items = [self.root, self.item]


class TreeAPIHarmonizerCommonTests(object):
    ''' Tests that should succeed for all tree controls and all styles. '''

    def testGetItemType(self):
        self.assertEqual(0, self.tree.GetItemType(self.item))

    def testGetItemImage_DefaultIcon(self):
        self.assertEqual(-1, self.tree.GetItemImage(self.item))

    def testGetItemImage_SelectedIcon(self):
        self.assertEqual(-1, 
            self.tree.GetItemImage(self.item, wx.TreeItemIcon_Selected))

    def testGetItemImage_DefaultIcon_OtherColumn(self):
        self.assertEqual(-1, self.tree.GetItemImage(self.item, column=1))

    def testGetItemImage_SelectedIcon_OtherColumn(self):
        self.assertEqual(-1, 
            self.tree.GetItemImage(self.item, wx.TreeItemIcon_Selected, 1))

    def testSetItemImage_DefaultIcon(self):
        self.tree.SetItemImage(self.item, -1)
        self.assertEqual(-1, self.tree.GetItemImage(self.item))

    def testSetItemImage_SelectedIcon(self):
        self.tree.SetItemImage(self.item, -1, wx.TreeItemIcon_Selected)
        self.assertEqual(-1, 
            self.tree.GetItemImage(self.item, wx.TreeItemIcon_Selected))

    def testSetItemImage_DefaultIcon_OtherColumn(self):
        self.tree.SetItemImage(self.item, -1, column=1)
        self.assertEqual(-1, self.tree.GetItemImage(self.item, column=1))

    def testSetItemImage_SelectedIcon_OtherColumn(self):
        self.tree.SetItemImage(self.item, -1, wx.TreeItemIcon_Selected, 1)
        self.assertEqual(-1, 
            self.tree.GetItemImage(self.item, wx.TreeItemIcon_Selected, 1))


class TreeAPIHarmonizerNoTreeListCtrlCommonTests(object):
    ''' Tests that should succeed for all tree controls, except the 
        TreeListCtrl, and all styles. '''

    def testGetMainWindow(self):
        self.assertEqual(self.tree, self.tree.GetMainWindow())

    def testGetColumnCount(self):
        self.assertEqual(0, self.tree.GetColumnCount())


class TreeAPIHarmonizerSingleSelectionTests(object):
    ''' Tests that should succeed for all tree controls when in single 
        selection mode (which is the default selection mode). '''

    def testUnselectAll(self):
        self.tree.SelectItem(self.item)
        self.tree.UnselectAll()
        self.assertEqual([], self.tree.GetSelections())

    def testGetSelections_NoSelection(self):
        self.tree.UnselectAll()
        self.assertEqual([], self.tree.GetSelections())

    def testGetSelections_OneSelectedItem(self):
        self.tree.UnselectAll()
        self.tree.SelectItem(self.item)
        self.assertEqual([self.item], self.tree.GetSelections())


class TreeAPIHarmonizerMultipleSelectionTests(object):
    ''' Tests that should succeed for all tree controls when in multiple 
        selection mode. '''

    style = wx.TR_DEFAULT_STYLE | wx.TR_MULTIPLE
    
    def testUnselectAll(self):
        self.tree.SelectItem(self.item)
        self.tree.UnselectAll()
        self.assertEqual([], self.tree.GetSelections())

    def testGetSelections_NoSelection(self):
        self.tree.UnselectAll()
        self.assertEqual([], self.tree.GetSelections())

    def testGetSelections_OneSelectedItem(self):
        self.tree.UnselectAll()
        self.tree.SelectItem(self.item)
        self.assertEqual([self.item], self.tree.GetSelections())

    def testGetSelections_TwoSelectedItems(self):
        item2 = self.tree.AppendItem(self.root, 'item 2')
        self.tree.ExpandAll()
        self.tree.UnselectAll()
        self.tree.SelectItem(item2)
        self.tree.SelectItem(self.item)
        self.assertEqual([self.item, item2], self.tree.GetSelections())



class TreeAPIHarmonizerVisibleRootTests(object):
    ''' Tests that should succeed for all tree controls when the root item
        is not hidden. '''

    def testGetCount(self):
        self.assertEqual(len(self.items), self.tree.GetCount())

    def testSelectRoot(self):
        self.tree.SelectItem(self.root)
        self.assertEqual([self.root], self.tree.GetSelections())


class TreeAPIHarmonizerHiddenRootTests(object):
    ''' Tests that should succeed for all tree controls when the root item
        is hidden. '''

    style = wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT

    def testGetCount(self):
        self.assertEqual(len(self.items) - 1, self.tree.GetCount())

    def testSelectRoot(self):
        self.tree.SelectItem(self.root)
        self.assertEqual([], self.tree.GetSelections())



class TreeAPIHarmonizerWithTreeCtrlTestCase(TreeAPIHarmonizerTestCase):
    TreeClass = wx.TreeCtrl


class TreeAPIHarmonizerWithTreeCtrlCommonTests( \
        TreeAPIHarmonizerCommonTests,
        TreeAPIHarmonizerNoTreeListCtrlCommonTests):
    pass


class TreeAPIHarmonizerWithTreeCtrl_SingleSelection( \
        TreeAPIHarmonizerWithTreeCtrlCommonTests, 
        TreeAPIHarmonizerSingleSelectionTests,
        TreeAPIHarmonizerWithTreeCtrlTestCase):
    pass


class TreeAPIHarmonizerWithTreeCtrl_MultipleSelection( \
        TreeAPIHarmonizerWithTreeCtrlCommonTests, 
        TreeAPIHarmonizerMultipleSelectionTests, 
        TreeAPIHarmonizerWithTreeCtrlTestCase):
    pass


class TreeAPIHarmonizerWithTreeCtrl_VisibleRoot( \
        TreeAPIHarmonizerWithTreeCtrlCommonTests, 
        TreeAPIHarmonizerVisibleRootTests,
        TreeAPIHarmonizerWithTreeCtrlTestCase):
    pass


class TreeAPIHarmonizerWithTreeCtrl_HiddenRoot( \
        TreeAPIHarmonizerWithTreeCtrlCommonTests, 
        TreeAPIHarmonizerHiddenRootTests,
        TreeAPIHarmonizerWithTreeCtrlTestCase):
    pass


class TreeAPIHarmonizerWithTreeListCtrlTestCase(TreeAPIHarmonizerTestCase):
    TreeClass = wx.gizmos.TreeListCtrl

    def populateTree(self):
        self.tree.AddColumn('Column')
        super(TreeAPIHarmonizerWithTreeListCtrlTestCase, self).populateTree()


class TreeAPIHarmonizerWithTreeListCtrlCommonTests( \
        TreeAPIHarmonizerCommonTests):

    def testGetColumnCount(self):
        self.assertEqual(1, self.tree.GetColumnCount())

    def testGetMainWindow(self):
        self.assertNotEqual(self.tree, self.tree.GetMainWindow())


class TreeAPIHarmonizerWithTreeListCtrl_SingleSelection( \
        TreeAPIHarmonizerWithTreeListCtrlCommonTests, 
        TreeAPIHarmonizerSingleSelectionTests,
        TreeAPIHarmonizerWithTreeListCtrlTestCase):
    pass


class TreeAPIHarmonizerWithTreeListCtrl_MultipleSelection( \
        TreeAPIHarmonizerWithTreeListCtrlCommonTests, 
        TreeAPIHarmonizerMultipleSelectionTests,
        TreeAPIHarmonizerWithTreeListCtrlTestCase):

    def testGetSelections_TwoSelectedItems(self):
        ''' Override TreeAPIHarmonizerMultipleSelectionTests.-
            testGetSelections_TwoSelectedItems, because 
            TreeListCtrl.SelectItem needs an extra parameter. '''
        self.tree.UnselectAll()
        item2 = self.tree.AppendItem(self.root, 'item 2')
        self.tree.SelectItem(self.item)
        self.tree.SelectItem(item2, unselect_others=False)
        self.assertEqual([self.item, item2], self.tree.GetSelections())


class TreeAPIHarmonizerWithTreeListCtrl_VisibleRoot( \
        TreeAPIHarmonizerWithTreeListCtrlCommonTests, 
        TreeAPIHarmonizerVisibleRootTests,
        TreeAPIHarmonizerWithTreeListCtrlTestCase):
    pass


class TreeAPIHarmonizerWithTreeListCtrl_HiddenRoot( \
        TreeAPIHarmonizerWithTreeListCtrlCommonTests, 
        TreeAPIHarmonizerHiddenRootTests,
        TreeAPIHarmonizerWithTreeListCtrlTestCase):
    pass


class TreeAPIHarmonizerWithCustomTreeCtrlTestCase(TreeAPIHarmonizerTestCase):
    TreeClass = wx.lib.customtreectrl.CustomTreeCtrl


class TreeAPIHarmonizerWithCustomTreeCtrlCommonTests( \
        TreeAPIHarmonizerCommonTests, 
        TreeAPIHarmonizerNoTreeListCtrlCommonTests):

    def testGetCheckItemType(self):
        item = self.tree.AppendItem(self.root, 'item', ct_type=1)
        self.assertEqual(1, self.tree.GetItemType(item))

    def testGetRadioItemType(self):
        item = self.tree.AppendItem(self.root, 'item', ct_type=2)
        self.assertEqual(2, self.tree.GetItemType(item))
        


class TreeAPIHarmonizerWithCustomTreeCtrl_SingleSelection( \
        TreeAPIHarmonizerWithCustomTreeCtrlCommonTests, 
        TreeAPIHarmonizerSingleSelectionTests,
        TreeAPIHarmonizerWithCustomTreeCtrlTestCase):
    pass


class TreeAPIHarmonizerWithCustomTreeCtrl_MultipleSelection( \
        TreeAPIHarmonizerWithCustomTreeCtrlCommonTests, 
        TreeAPIHarmonizerMultipleSelectionTests,
        TreeAPIHarmonizerWithCustomTreeCtrlTestCase):
    pass


class TreeAPIHarmonizerWithCustomTreeCtrl_VisibleRoot( \
        TreeAPIHarmonizerWithCustomTreeCtrlCommonTests, 
        TreeAPIHarmonizerVisibleRootTests,
        TreeAPIHarmonizerWithCustomTreeCtrlTestCase):
    pass


class TreeAPIHarmonizerWithCustomTreeCtrl_HiddenRoot( \
        TreeAPIHarmonizerWithCustomTreeCtrlCommonTests, 
        TreeAPIHarmonizerHiddenRootTests,
        TreeAPIHarmonizerWithCustomTreeCtrlTestCase):
    pass


# TreeHelper tests

class TreeHelperTestCase(unittest.TestCase):
    style = wx.TR_DEFAULT_STYLE

    def setUp(self):
        self.frame = wx.Frame(None)
        class HelperTreeCtrl(treemixin.TreeHelper, 
                             treemixin.TreeAPIHarmonizer, self.TreeClass):
            pass
        self.tree = HelperTreeCtrl(self.frame, style=self.style)
        self.populateTree()

    def populateTree(self):
        self.root = self.tree.AddRoot('Root')
        self.item = self.tree.AppendItem(self.root, 'Item')
        self.child = self.tree.AppendItem(self.item, 'Child')


class TreeHelperVisibleRootTests(object):
    def testIntegerIndexRootItem(self):
        self.assertEqual(0, self.tree.ItemIndex(self.root, tupleIndex=False))

    def testIntegerIndexRegularItem(self):
        self.assertEqual(1, self.tree.ItemIndex(self.item, tupleIndex=False))

    def testIntegerIndexChild(self):
        self.assertEqual(2, self.tree.ItemIndex(self.child, tupleIndex=False))

    def testTupleIndexRootItem(self):
        self.assertEqual((), self.tree.ItemIndex(self.root))

    def testTupleIndexRegularItem(self):
        self.assertEqual((0,), self.tree.ItemIndex(self.item))

    def testTupleIndexChild(self):
        self.assertEqual((0,0), self.tree.ItemIndex(self.child))


class TreeHelperHiddenRootTests(object):
    style = wx.TR_HIDE_ROOT

    def testIntegerIndexRootItem(self):
        self.assertEqual(None, self.tree.ItemIndex(self.root, tupleIndex=False))

    def testIntegerIndexRegularItem(self):
        self.assertEqual(0, self.tree.ItemIndex(self.item, tupleIndex=False))

    def testIntegerIndexChild(self):
        self.assertEqual(1, self.tree.ItemIndex(self.child, tupleIndex=False))

    def testTupleIndexRootItem(self):
        self.assertEqual((), self.tree.ItemIndex(self.root))

    def testTupleIndexRegularItem(self):
        self.assertEqual((0,), self.tree.ItemIndex(self.item))

    def testTupleIndexChild(self):
        self.assertEqual((0,0), self.tree.ItemIndex(self.child))


class TreeHelperWithTreeCtrlTestCase(TreeHelperTestCase):
    TreeClass = wx.TreeCtrl


class TreeHelperWithTreeCtrl_VisibleRoot(TreeHelperVisibleRootTests, 
        TreeHelperWithTreeCtrlTestCase):
    pass


class TreeHelperWithTreeCtrl_HiddenRoot(TreeHelperHiddenRootTests, 
        TreeHelperWithTreeCtrlTestCase):
    pass


class TreeHelperWithTreeListCtrlTestCase(TreeHelperTestCase):
    TreeClass = wx.gizmos.TreeListCtrl

    def populateTree(self):
        self.tree.AddColumn('Column')
        super(TreeHelperWithTreeListCtrlTestCase, self).populateTree()


class TreeHelperWithTreeListCtrl_VisibleRoot(TreeHelperVisibleRootTests, 
        TreeHelperWithTreeListCtrlTestCase):
    pass


class TreeHelperWithTreeListCtrl_HiddenRoot(TreeHelperHiddenRootTests, 
        TreeHelperWithTreeListCtrlTestCase):
    pass

class TreeHelperWithCustomTreeCtrlTestCase(TreeHelperTestCase):
    TreeClass = wx.lib.customtreectrl.CustomTreeCtrl


class TreeHelperWithCustomTreeCtrl_VisibleRoot(TreeHelperVisibleRootTests, 
        TreeHelperWithCustomTreeCtrlTestCase):
    pass


class TreeHelperWithCustomTreeCtrl_HiddenRoot(TreeHelperHiddenRootTests, 
        TreeHelperWithCustomTreeCtrlTestCase):
    pass


# ExpansionState tests

class ExpansionStateTreeCtrl(treemixin.ExpansionState, wx.TreeCtrl):
    pass


class GetExpansionStateTestCase(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(None)
        self.tree = ExpansionStateTreeCtrl(self.frame)

    def testEmptyTree(self):
        self.assertEqual([], self.tree.GetExpansionState())
        
    def testRoot(self):
        self.tree.AddRoot('Root item')
        self.assertEqual([], self.tree.GetExpansionState())

    def testRoot_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        self.assertEqual([], self.tree.GetExpansionState())
        
    def testExpandedRoot_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        self.tree.Expand(root)
        self.assertEqual([()], self.tree.GetExpansionState())

    def testExpandedRoot_Child_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        self.tree.Expand(root)
        # Property should work too:
        self.assertEqual([()], self.tree.ExpansionState) 

    def testRoot_ExpandedChild_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        self.tree.Expand(child)
        self.assertEqual([], self.tree.GetExpansionState())

    def testExpandedRoot_ExpandedChild_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        self.tree.Expand(child)
        self.tree.Expand(root)
        self.assertEqual([(), (0,)], self.tree.GetExpansionState())

    def testExpandedRoot_ExpandedChild_ExpandedChild(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        grandGrandChild = self.tree.AppendItem(grandChild, 'Grandgrandchild')
        self.tree.Expand(root)
        self.tree.Expand(child)
        self.tree.Expand(grandChild)
        self.assertEqual([(), (0,), (0,0)], self.tree.GetExpansionState())


class SetExpansionStateTestCase(unittest.TestCase):
    def setUp(self):
        self.frame = wx.Frame(None)
        self.tree = ExpansionStateTreeCtrl(self.frame)

    def testEmptyTree(self):
        self.tree.SetExpansionState([])

    def testRoot(self):
        root = self.tree.AddRoot('Root item')
        self.tree.SetExpansionState([])
        self.failIf(self.tree.IsExpanded(root))
    
    def testRoot_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        self.tree.SetExpansionState([])
        self.failIf(self.tree.IsExpanded(root))

    def testExpandedRoot_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        self.tree.ExpansionState = [()] # Property should work too
        self.failUnless(self.tree.IsExpanded(root))

    def testExpandedRoot_Child_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        self.tree.SetExpansionState([()])
        self.failIf(self.tree.IsExpanded(child))

    def testExpandedRoot_ExpandedChild_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        self.tree.SetExpansionState([(), (0,)])
        self.failUnless(self.tree.IsExpanded(child))

    def testRoot_ExpandedChild_Child(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        self.tree.SetExpansionState([(0,)])
        self.failIf(self.tree.IsExpanded(child))

    def testExpandedRoot_ExpandedChild_ExpandedChild(self):
        root = self.tree.AddRoot('Root item')
        child = self.tree.AppendItem(root, 'Child')
        grandChild = self.tree.AppendItem(child, 'Grandchild')
        grandGrandChild = self.tree.AppendItem(grandChild, 'Grandgrandchild')
        self.tree.SetExpansionState([(), (0,), (0,0)])
        self.failUnless(self.tree.IsExpanded(grandChild))


if __name__ == '__main__':
    app = wx.App(False)
    unittest.main()


