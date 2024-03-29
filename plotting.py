# imports from installed libraries
import matplotlib.pyplot as plt
import numpy as np
import torch
import os


# Plot the confusion matrix
def plot_confusion_matrix(conf_mat,
                          hide_spines=False,
                          hide_ticks=False,
                          figsize=None,
                          cmap=None,
                          colorbar=False,
                          show_absolute=True,
                          show_normed=False,
                          class_names=None):
    if not (show_absolute or show_normed):
        raise AssertionError('Both show_absolute and show_normed are False')
    if class_names is not None and len(class_names) != len(conf_mat):
        raise AssertionError('len(class_names) should be equal to number of'
                             'classes in the dataset')

    total_samples = conf_mat.sum(axis=1)[:, np.newaxis]
    normed_conf_mat = conf_mat.astype('float') / total_samples

    if figsize is None:
        figsize = (len(conf_mat) * 0.3, len(conf_mat) * 0.3)

    fig, ax = plt.subplots(figsize=figsize)
    ax.grid(False)
    if cmap is None:
        cmap = plt.cm.Blues

    if show_normed:
        matshow = ax.matshow(normed_conf_mat, cmap=cmap)
    else:
        matshow = ax.matshow(conf_mat, cmap=cmap)

    if colorbar:
        fig.colorbar(matshow)

    for i in range(conf_mat.shape[0]):
        for j in range(conf_mat.shape[1]):
            cell_text = ""
            if show_absolute:
                cell_text += format(conf_mat[i, j], 'd')
                if show_normed:
                    cell_text += "\n" + '('
                    cell_text += format(normed_conf_mat[i, j], '.2f') + ')'
            else:
                cell_text += format(normed_conf_mat[i, j], '.2f')
            ax.text(x=j,
                    y=i,
                    s=cell_text,
                    va='center',
                    ha='center',
                    color="white" if normed_conf_mat[i, j] > 0.5 else "black")

    if class_names is not None:
        tick_marks = np.arange(len(class_names))
        plt.xticks(tick_marks, class_names, rotation=90)
        plt.yticks(tick_marks, class_names)

    if hide_spines:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_ticks_position('bottom')
    if hide_ticks:
        ax.axes.get_yaxis().set_ticks([])
        ax.axes.get_xaxis().set_ticks([])

    plt.xlabel('predicted label')
    plt.ylabel('true label')
    return fig, ax


# def plot_training_loss(minibatch_loss_list, num_epochs, iter_per_epoch,
#                        results_dir=None, averaging_iterations=100):
#
#     plt.figure()
#     ax1 = plt.subplot(1, 1, 1)
#     ax1.plot(range(len(minibatch_loss_list)),
#              minibatch_loss_list, label='Minibatch Loss')
#
#     if len(minibatch_loss_list) > 1000:
#         ax1.set_ylim([
#             0, np.max(minibatch_loss_list[1000:])*1.5
#             ])
#     ax1.set_xlabel('Iterations')
#     ax1.set_ylabel('Loss')
#
#     ax1.plot(np.convolve(minibatch_loss_list,
#                          np.ones(averaging_iterations,)/averaging_iterations,
#                          mode='valid'),
#              label='Running Average')
#     ax1.legend()
#
#     ###################
#     # Set scond x-axis
#     ax2 = ax1.twiny()
#     newlabel = list(range(num_epochs+1))
#
#     newpos = [e*iter_per_epoch for e in newlabel]
#
#     ax2.set_xticks(newpos[::10])
#     ax2.set_xticklabels(newlabel[::10])
#
#     ax2.xaxis.set_ticks_position('bottom')
#     ax2.xaxis.set_label_position('bottom')
#     ax2.spines['bottom'].set_position(('outward', 45))
#     ax2.set_xlabel('Epochs')
#     ax2.set_xlim(ax1.get_xlim())
#     ###################
#
#     plt.tight_layout()
#
#     if results_dir is not None:
#         image_path = os.path.join(results_dir, 'plot_training_loss.pdf')
#         plt.savefig(image_path)


# # Plot the accuracy of the training and validation set
# def plot_accuracy(train_accuracy_list, valid_accuracy_list, results_dir):
#     num_epochs = len(train_accuracy_list)
#
#     plt.plot(np.arange(1, num_epochs + 1),
#              train_accuracy_list, label='Training')
#     plt.plot(np.arange(1, num_epochs + 1),
#              valid_accuracy_list, label='Validation')
#
#     plt.xlabel('Epoch')
#     plt.ylabel('Accuracy')
#     plt.legend()
#
#     plt.tight_layout()
#
#     if results_dir is not None:
#         image_path = os.path.join(
#             results_dir, 'plot_acc_training_validation.pdf')
#         plt.savefig(image_path)
