#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "functions.h"
#include <QMainWindow>
#include <QWidget>
#include <QListWidget>
#include <QListWidgetItem>
#include <QList>
#include <QKeyEvent>
#include <QEvent>
#include <QProcess>
#include <QToolTip>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    void run(int index);
    void reset();
    void keyReleaseEvent(QKeyEvent *event);
    void keyPressEvent(QKeyEvent *event);

private slots:
    void on_lineEdit_textChanged(const QString &arg1);

    void on_listWidget_itemClicked();

    void toggle();

private:
    Ui::MainWindow *ui;
    Searcher *searcher;
    QList <QStringList> result;
    int sum;
};

#endif // MAINWINDOW_H
