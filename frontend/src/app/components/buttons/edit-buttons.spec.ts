import { ViewButtons } from '#components/buttons';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('ViewButtons', () => {
  let component: ViewButtons;
  let fixture: ComponentFixture<ViewButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewButtons],
    }).compileComponents();

    fixture = TestBed.createComponent(ViewButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
