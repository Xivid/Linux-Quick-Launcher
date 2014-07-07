#include "mainwindow.h"
#include "ui_mainwindow.h"
//#include "functions.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->sum = 0;
    this->result.clear();
    ui->listWidget->clear();
    ui->listWidget->hide();
    this->setGeometry(100, 50, 256, 27);
    this->setFixedSize(QSize(256, 27));
    this->setWindowFlags(Qt::FramelessWindowHint);
    ui->lineEdit->setFocusPolicy(Qt::StrongFocus);
    ui->listWidget->setFocusPolicy(Qt::StrongFocus);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::reset()
{
    ui->lineEdit->setText("");
    this->sum = 0;
    this->result.clear();
    ui->listWidget->clear();
    ui->listWidget->hide();
    this->setFixedSize(QSize(256, 27));
    QToolTip::hideText();
}

void MainWindow::run(int index)
{
    QProcess *poc = new QProcess;
    poc->start("yelp");
    reset();
}

void MainWindow::on_lineEdit_textChanged(const QString &arg1)
{

    QString keyword = ui->lineEdit->text();
    if (keyword == ":q")
        this->close();

    //getlist(this->result, keyword);
    this->result.clear();
    for (int i = 0; i < 20; i++)
        this->result.append(QString(i));
    this->sum = this->result.size();

    if (keyword != "" && this->sum != 0)
    {
        ui->listWidget->clear();
        //QListWidgetItem item;
        for (int i = 0; i < this->sum + 10; i++)
        {
            //item.setText(this->result[i]);
            //setText(this->result[i]);
            ui->listWidget->insertItem(i, "App");
        }
        ui->listWidget->setFixedSize(QSize(256,  int(20 * this->sum)));
        this->setFixedSize(QSize(256, 27 + int(19.2 * this->sum)));
        ui->listWidget->show();
    }
    else
    {
        this->result.clear();
        this->sum = 0;
        ui->listWidget->clear();
        ui->listWidget->hide();
        this->setFixedSize(QSize(256, 27));
    }
}

void MainWindow::keyPressEvent(QKeyEvent *event)
{
    if (ui->listWidget->hasFocus() && event->key() == Qt::Key_Up && ui->listWidget->currentRow() == 0)
        ui->lineEdit->setFocus();
}

void MainWindow::keyReleaseEvent(QKeyEvent *event)
{
    if (ui->lineEdit->hasFocus())
    {
        switch (event->key())
        {
        case Qt::Key_Return:
            if (this->sum)
                run(0);
            break;
        case Qt::Key_Escape:
            reset();
            break;
        case Qt::Key_Down:
            if (this->sum)
            {
                ui->listWidget->setFocus();
                ui->listWidget->setCurrentRow(0);
                QToolTip::showText(QPoint(100 + 128, 80), "TAT", ui->listWidget, QRect(100, 50 + 27, 256, int(20 * this->sum)));
            }
            break;
        default:
            break;
        }
    }
    else if (ui->listWidget->hasFocus())
    {
        int w, h = 0;
        if (ui->listWidget->currentRow() - h > 20)
            w = 77 + 384;
        else
            w = 77 + int(19.2 * (ui->listWidget->currentRow() - h));

        switch (event->key())
        {
        case Qt::Key_Return:
            run(ui->listWidget->currentRow());
            break;
        case Qt::Key_Escape:
            reset();
            break;
        default:
            QToolTip::showText(QPoint(100 + 128, w), "QAQ", ui->listWidget, QRect(100, 77 + 292, 100, 77 + 292));//
            break;
        }
    }
}

void MainWindow::on_listWidget_itemClicked(QListWidgetItem *item)
{
    run(ui->listWidget->currentRow());
}
